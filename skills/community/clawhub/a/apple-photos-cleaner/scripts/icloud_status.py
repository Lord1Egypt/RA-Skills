#!/usr/bin/env python3
"""
Check iCloud sync status across the Apple Photos library.

Reports on which photos are synced, local-only, cloud-only,
download status, and potential sync issues.
"""

import sys
from typing import Any

from _common import (
    PhotosDB,
    _safe_col,
    coredata_to_local,
    display_name,
    format_size,
    has_timezone_offset,
    original_filename_sql,
    run_script,
    tz_offset_sql,
)
from _schema import FILE_SIZE, ORIGINAL_FILENAME, Degradation, get_schema

# Schema contract (T1.4): see _schema. Missing required → exit 5; missing optional → `degraded`.
REQUIRED_COLUMNS: tuple[str, ...] = (
    "ZASSET.ZDATECREATED",
    "ZASSET.ZFAVORITE",
    "ZASSET.ZFILENAME",
    "ZASSET.ZKIND",
    "ZASSET.ZTRASHEDSTATE",
    *FILE_SIZE,
)
OPTIONAL_COLUMNS: dict[str, tuple[str, ...]] = {
    "original_filenames": ORIGINAL_FILENAME,
    "icloud": ("asset.cloud_local_state",),
    "ownership": ("asset.cloud_is_my_asset",),
    "downloadable": ("asset.cloud_is_downloadable",),
}

# iCloud local state values
CLOUD_STATE_NOT_UPLOADED = 0
CLOUD_STATE_SYNCED = 1

CLOUD_STATE_NAMES = {
    0: "not_uploaded",
    1: "synced",
}


def analyze_icloud_status(
    db_path: str | None = None,
) -> dict[str, Any]:
    """
    Analyze iCloud sync status of all assets.

    Returns breakdown of sync states, storage impact, and
    assets that might have sync issues.
    """
    with PhotosDB(db_path, require=REQUIRED_COLUMNS, operation="iCloud status") as conn:
        name_col = original_filename_sql(get_schema(conn))
        cursor = conn.cursor()
        tz_available = has_timezone_offset(cursor)

        # Check available columns
        degraded = Degradation(get_schema(conn))
        degraded.check("original_filenames", *OPTIONAL_COLUMNS["original_filenames"])
        has_cloud_state = degraded.check("icloud", *OPTIONAL_COLUMNS["icloud"])
        has_cloud_asset = degraded.check("ownership", *OPTIONAL_COLUMNS["ownership"])
        has_downloadable = degraded.check("downloadable", *OPTIONAL_COLUMNS["downloadable"])

        if not has_cloud_state:
            return {
                "degraded": degraded.entries,
                "error": "iCloud columns not found in this database version.",
                "icloud_enabled": False,
                "summary": {
                    "total_assets": 0,
                    "synced_count": 0,
                    "local_only_count": 0,
                },
            }

        # Build query
        select_cols = [
            "a.Z_PK",
            "a.ZFILENAME",
            name_col,
            "a.ZDATECREATED",
            "a.ZKIND",
            "a.ZFAVORITE",
            "a.ZCLOUDLOCALSTATE",
            "aa.ZORIGINALFILESIZE",
            f"{tz_offset_sql(tz_available)} AS tz_offset",
        ]
        if has_cloud_asset:
            select_cols.append("a.ZCLOUDISMYASSET")
        if has_downloadable:
            select_cols.append("a.ZCLOUDISDOWNLOADABLE")

        query = f"""
            SELECT {", ".join(select_cols)}
            FROM ZASSET a
            LEFT JOIN ZADDITIONALASSETATTRIBUTES aa ON a.Z_PK = aa.ZASSET
            WHERE a.ZTRASHEDSTATE != 1
            ORDER BY a.ZDATECREATED DESC
        """
        cursor.execute(query)

        synced_count = 0
        synced_size = 0
        local_only_count = 0
        local_only_size = 0
        by_state: dict[str, int] = {}
        by_kind: dict[str, dict] = {}  # photo/video -> synced/local
        by_year: dict[str, dict] = {}
        local_only_large: list[dict] = []
        my_assets = 0
        other_assets = 0
        downloadable_count = 0

        for row in cursor.fetchall():
            rd = dict(row)
            cloud_state = _safe_col(rd, "ZCLOUDLOCALSTATE", 0) or 0
            size = rd.get("ZORIGINALFILESIZE") or 0
            kind = rd.get("ZKIND", 0) or 0
            kind_name = "photo" if kind == 0 else "video"

            state_name = CLOUD_STATE_NAMES.get(cloud_state, f"state_{cloud_state}")
            by_state[state_name] = by_state.get(state_name, 0) + 1

            if kind_name not in by_kind:
                by_kind[kind_name] = {"synced": 0, "local_only": 0, "synced_size": 0, "local_size": 0}

            created = coredata_to_local(rd["ZDATECREATED"], rd["tz_offset"])
            yr = str(created.year) if created else "Unknown"
            if yr not in by_year:
                by_year[yr] = {"synced": 0, "local_only": 0, "synced_size": 0, "local_size": 0}

            is_mine = _safe_col(rd, "ZCLOUDISMYASSET", 1)
            if is_mine:
                my_assets += 1
            else:
                other_assets += 1

            if _safe_col(rd, "ZCLOUDISDOWNLOADABLE", 0):
                downloadable_count += 1

            if cloud_state == CLOUD_STATE_SYNCED:
                synced_count += 1
                synced_size += size
                by_kind[kind_name]["synced"] += 1
                by_kind[kind_name]["synced_size"] += size
                by_year[yr]["synced"] += 1
                by_year[yr]["synced_size"] += size
            else:
                local_only_count += 1
                local_only_size += size
                by_kind[kind_name]["local_only"] += 1
                by_kind[kind_name]["local_size"] += size
                by_year[yr]["local_only"] += 1
                by_year[yr]["local_size"] += size

                # Track large local-only items
                if size > 10_000_000:  # >10 MB
                    local_only_large.append(
                        {
                            "id": rd["Z_PK"],
                            "filename": rd["ZFILENAME"],
                            "original_filename": rd["original_filename"],
                            "created": created.isoformat() if created else None,
                            "size": size,
                            "size_formatted": format_size(size),
                            "kind": kind_name,
                            "is_favorite": bool(rd.get("ZFAVORITE")),
                        }
                    )

        total = synced_count + local_only_count
        total_size = synced_size + local_only_size
        local_only_large.sort(key=lambda x: x["size"], reverse=True)

        return {
            "degraded": degraded.entries,
            "icloud_enabled": synced_count > 0,
            "by_state": by_state,
            "by_kind": {
                k: {
                    **v,
                    "synced_size_formatted": format_size(v["synced_size"]),
                    "local_size_formatted": format_size(v["local_size"]),
                }
                for k, v in by_kind.items()
            },
            "by_year": [
                {
                    "year": yr,
                    "synced": info["synced"],
                    "local_only": info["local_only"],
                    "synced_size_formatted": format_size(info["synced_size"]),
                    "local_size_formatted": format_size(info["local_size"]),
                }
                for yr, info in sorted(by_year.items(), reverse=True)
            ],
            "local_only_large": local_only_large[:50],
            "summary": {
                "total_assets": total,
                "total_storage": total_size,
                "total_storage_formatted": format_size(total_size),
                "synced_count": synced_count,
                "synced_pct": round(100 * synced_count / max(1, total), 1),
                "synced_storage": synced_size,
                "synced_storage_formatted": format_size(synced_size),
                "local_only_count": local_only_count,
                "local_only_pct": round(100 * local_only_count / max(1, total), 1),
                "local_only_storage": local_only_size,
                "local_only_storage_formatted": format_size(local_only_size),
                "my_assets": my_assets,
                "other_assets": other_assets,
                "downloadable_count": downloadable_count,
                "large_local_only_count": len(local_only_large),
            },
        }


def format_summary(data: dict[str, Any]) -> str:
    """Format human-readable summary."""
    lines = []
    s = data["summary"]

    if "error" in data:
        lines.append(f"⚠️  {data['error']}")
        return "\n".join(lines)

    lines.append("☁️  iCLOUD SYNC STATUS")
    lines.append("=" * 50)

    if not data["icloud_enabled"]:
        lines.append("iCloud Photos sync appears to be disabled.")
        lines.append(f"Total local assets: {s['total_assets']:,}")
        lines.append(f"Total storage:      {s['total_storage_formatted']}")
        return "\n".join(lines)

    lines.append(f"Total assets:        {s['total_assets']:,}  ({s['total_storage_formatted']})")
    lines.append(f"Synced to iCloud:    {s['synced_count']:,}  ({s['synced_pct']}%)  {s['synced_storage_formatted']}")
    lines.append(
        f"Local only:          {s['local_only_count']:,}  ({s['local_only_pct']}%)  {s['local_only_storage_formatted']}"
    )
    lines.append(f"My assets:           {s['my_assets']:,}")
    lines.append(f"Others' assets:      {s['other_assets']:,}")

    if s.get("downloadable_count"):
        lines.append(f"Downloadable (cloud): {s['downloadable_count']:,}")

    if data["by_kind"]:
        lines.append("")
        lines.append("By content type:")
        for kind, info in sorted(data["by_kind"].items()):
            lines.append(
                f"  {kind:10s}  synced: {info['synced']:>6,} ({info['synced_size_formatted']:>10})  "
                f"local: {info['local_only']:>6,} ({info['local_size_formatted']:>10})"
            )

    if data["by_year"]:
        lines.append("")
        lines.append("By year:")
        lines.append(f"  {'Year':<8} {'Synced':>8} {'Local':>8}")
        for yr in data["by_year"][:10]:
            lines.append(f"  {yr['year']:<8} {yr['synced']:>8,} {yr['local_only']:>8,}")

    if data["local_only_large"]:
        lines.append("")
        lines.append(f"Large local-only items (>10 MB): {s['large_local_only_count']}")
        for item in data["local_only_large"][:10]:
            fav = "⭐" if item["is_favorite"] else "  "
            lines.append(f"  {fav} {display_name(item):40s} {item['size_formatted']:>10}  ({item['kind']})")

    return "\n".join(lines)


def main():
    return run_script(
        description="Check iCloud sync status in Apple Photos",
        analyze_fn=lambda db_path, _args: analyze_icloud_status(db_path=db_path),
        format_fn=format_summary,
    )


if __name__ == "__main__":
    sys.exit(main())
