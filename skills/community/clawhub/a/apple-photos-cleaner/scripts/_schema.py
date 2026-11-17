#!/usr/bin/env python3
"""
Schema registry for the Photos database (ROADMAP T1.1).

Apple renames and adds Core Data columns between macOS releases. This module is
the only place that inspects the schema: it reads the table list once, reads a
table's columns the first time something asks, and maps *logical* names such as
``face.person_fk`` to whichever physical column this library actually has.

When Apple renames a column, add the new name to the front of its candidate
tuple in LOGICAL_COLUMNS. Code that builds SQL with ``schema.col(...)`` follows
automatically.

Every name the registry accepts is either a logical name from LOGICAL_COLUMNS or
a physical ``"ZTABLE.ZCOLUMN"`` reference (graceful degradation, T1.4). Scripts
declare what they need:

- ``REQUIRED_COLUMNS``: the command cannot run without these. Pass them to
  ``PhotosDB(..., require=REQUIRED_COLUMNS)``; a missing one is exit code 5.
- ``OPTIONAL_COLUMNS``: ``{section: names}``. When any is missing, the script
  still runs, that section is computed without it (or is ``null``), and the
  result's ``degraded`` list says why (see Degradation).

Use ``PRAGMA table_info(...)`` here, never the ``pragma_table_info()``
table-valued function: older SQLite trips the read-only authorizer on it.
"""

import hashlib
import plistlib
import re
import sqlite3


class SchemaUnsupportedError(RuntimeError):
    """The Photos database lacks something this command cannot run without."""


# logical name -> (table, physical column candidates in preference order)
LOGICAL_COLUMNS: dict[str, tuple[str, tuple[str, ...]]] = {
    # ZASSET
    "asset.uuid": ("ZASSET", ("ZUUID",)),
    "asset.kind_subtype": ("ZASSET", ("ZKINDSUBTYPE",)),
    "asset.playback_style": ("ZASSET", ("ZPLAYBACKSTYLE",)),
    "asset.library_scope": ("ZASSET", ("ZLIBRARYSCOPE",)),
    "asset.shared_library_scope_id": ("ZASSET", ("ZSHAREDLIBRARYSCOPEIDENTIFIER",)),
    "asset.cloud_local_state": ("ZASSET", ("ZCLOUDLOCALSTATE",)),
    "asset.cloud_is_my_asset": ("ZASSET", ("ZCLOUDISMYASSET",)),
    "asset.cloud_is_downloadable": ("ZASSET", ("ZCLOUDISDOWNLOADABLE",)),
    # ZADDITIONALASSETATTRIBUTES
    "asset_attrs.tz_offset": ("ZADDITIONALASSETATTRIBUTES", ("ZTIMEZONEOFFSET",)),
    # ZCOMPUTEDASSETATTRIBUTES
    "computed.composition": ("ZCOMPUTEDASSETATTRIBUTES", ("ZPLEASANTCOMPOSITIONSCORE",)),
    # ZDETECTEDFACE (macOS 15 Sequoia renamed the foreign keys)
    "face.person_fk": ("ZDETECTEDFACE", ("ZPERSONFORFACE", "ZPERSON")),
    "face.asset_fk": ("ZDETECTEDFACE", ("ZASSETFORFACE", "ZASSET")),
    "face.quality": ("ZDETECTEDFACE", ("ZQUALITYMEASURE",)),
    "face.blur": ("ZDETECTEDFACE", ("ZBLURSCORE",)),
    "face.smile": ("ZDETECTEDFACE", ("ZSMILESCORE",)),
}


# Column groups scripts compose their contracts from.
QUALITY_SCORES: tuple[str, ...] = (
    "ZCOMPUTEDASSETATTRIBUTES.ZASSET",
    "ZCOMPUTEDASSETATTRIBUTES.ZFAILURESCORE",
    "ZCOMPUTEDASSETATTRIBUTES.ZNOISESCORE",
    "ZCOMPUTEDASSETATTRIBUTES.ZPLEASANTCOMPOSITIONSCORE",
    "ZCOMPUTEDASSETATTRIBUTES.ZPLEASANTLIGHTINGSCORE",
)
FACES: tuple[str, ...] = ("face.person_fk", "face.asset_fk", "ZPERSON.ZFULLNAME")
SCENES: tuple[str, ...] = ("ZSCENECLASSIFICATION.ZASSET", "ZSCENECLASSIFICATION.ZSCENENAME")
BURSTS: tuple[str, ...] = ("ZASSET.ZAVALANCHEKIND", "ZASSET.ZAVALANCHEPICKTYPE")
FILE_SIZE: tuple[str, ...] = ("ZADDITIONALASSETATTRIBUTES.ZASSET", "ZADDITIONALASSETATTRIBUTES.ZORIGINALFILESIZE")
# The name the user knows (IMG_1234.HEIC). ZASSET.ZFILENAME is Photos' internal storage name (a UUID on current macOS).
ORIGINAL_FILENAME: tuple[str, ...] = (
    "ZADDITIONALASSETATTRIBUTES.ZASSET",
    "ZADDITIONALASSETATTRIBUTES.ZORIGINALFILENAME",
)


def _virtual_module(sql: str) -> str:
    """The module of a ``CREATE VIRTUAL TABLE … USING module(…)`` statement, e.g. ``rtree``."""
    match = re.search(r"\bUSING\s+(\w+)", sql, re.IGNORECASE)
    return match[1].lower() if match else "unknown"


_PHYSICAL = re.compile(r"(Z\w*)\.(Z\w+)")


def resolve(name: str) -> tuple[str, tuple[str, ...]]:
    """(table, candidate columns) for a logical name or a physical "ZTABLE.ZCOLUMN"."""
    if name in LOGICAL_COLUMNS:
        return LOGICAL_COLUMNS[name]
    match = _PHYSICAL.fullmatch(name)
    if match:
        return match[1], (match[2],)
    raise KeyError(f"unknown schema name {name!r}: not in LOGICAL_COLUMNS and not ZTABLE.ZCOLUMN")


class SchemaRegistry:
    """What this Photos database contains, introspected once per connection."""

    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        rows = conn.execute("SELECT name, sql FROM sqlite_master WHERE type = 'table' ORDER BY name").fetchall()
        self._tables: tuple[str, ...] = tuple(row[0] for row in rows)
        # Virtual tables (Photos keeps an R*Tree, Z_RT_Asset_boundedByRect) are never connected to:
        # connecting prepares the module's own INSERTs, which the read-only authorizer refuses.
        self._virtual: dict[str, str] = {
            row[0]: _virtual_module(row[1]) for row in rows if (row[1] or "").upper().startswith("CREATE VIRTUAL TABLE")
        }
        self._columns: dict[str, frozenset[str]] = {}

    def tables(self) -> tuple[str, ...]:
        """All table names, sorted."""
        return self._tables

    def has_table(self, table: str) -> bool:
        return table in self._tables

    def is_virtual(self, table: str) -> bool:
        return table in self._virtual

    def columns(self, table: str) -> frozenset[str]:
        """Column names of *table*; empty if the table doesn't exist or is virtual."""
        if table not in self._columns:
            if not self.has_table(table) or self.is_virtual(table):
                return frozenset()
            quoted = '"' + table.replace('"', '""') + '"'
            rows = self._conn.execute(f"PRAGMA table_info({quoted})").fetchall()
            self._columns[table] = frozenset(row[1] for row in rows)
        return self._columns[table]

    def ddl(self) -> list[str]:
        """``CREATE TABLE`` statements for every table: the schema only, never rows."""
        rows = self._conn.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND sql IS NOT NULL ORDER BY name"
        ).fetchall()
        return [row[0] for row in rows]

    def fingerprint(self) -> str:
        """SHA-256 of every Core Data table and column name: identifies a schema, not a library.

        Only names are hashed, never rows, so it is safe to share in an issue.
        """
        names = sorted(
            [f"{table}.{column}" for table in self._tables if table.startswith("Z") for column in self.columns(table)]
            + [f"{table}.<virtual:{module}>" for table, module in self._virtual.items() if table.startswith("Z")]
        )
        return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()

    def model_version(self) -> int | None:
        """Photos' own data-model version (``PLModelVersion`` in Z_METADATA), or None if unreadable."""
        if not self.has_column("Z_METADATA", "Z_PLIST"):
            return None
        row = self._conn.execute("SELECT Z_PLIST FROM Z_METADATA LIMIT 1").fetchone()
        if not row or not row[0]:
            return None
        try:
            version = plistlib.loads(row[0]).get("PLModelVersion")
        except (plistlib.InvalidFileException, ValueError, TypeError, AttributeError):
            return None
        return version if isinstance(version, int) else None

    def has_column(self, table: str, column: str) -> bool:
        return column in self.columns(table)

    def col(self, name: str) -> str | None:
        """The physical column for *name*, or None if this library has none of its candidates."""
        table, candidates = resolve(name)
        present = self.columns(table)
        return next((column for column in candidates if column in present), None)

    def has(self, name: str) -> bool:
        return self.col(name) is not None

    def missing(self, *names: str) -> list[str]:
        """Human-readable "ZTABLE.ZCOLUMN" for each of *names* this library lacks."""
        return [describe(name) for name in names if not self.has(name)]

    def select(self, name: str, alias: str, as_: str | None = None) -> str:
        """SELECT-list term for an optional column: ``alias.COL``, or ``NULL AS COL`` when it is missing.

        *as_* names the result column either way (default: the column's own name).
        """
        column = self.col(name)
        if column is not None:
            return f"{alias}.{column}" + (f" AS {as_}" if as_ else "")
        return f"NULL AS {as_ or resolve(name)[1][0]}"

    def require(self, *names: str, operation: str) -> None:
        """Raise SchemaUnsupportedError naming every missing column."""
        missing = self.missing(*names)
        if missing:
            raise SchemaUnsupportedError(
                f"{', '.join(missing)} not found in this Photos database. {operation} cannot run without it. "
                "Please open an issue with your macOS version."
            )


# Photos data-model version ranges → macOS release (each major Photos release takes a block of 1000).
MODEL_VERSION_RANGES: tuple[tuple[int, int, str], ...] = (
    (13000, 13999, "macOS 10.15 Catalina"),
    (14000, 14999, "macOS 11 Big Sur"),
    (15000, 15999, "macOS 12 Monterey"),
    (16000, 16999, "macOS 13 Ventura"),
    (17000, 17999, "macOS 14 Sonoma"),
    (18000, 18999, "macOS 15 Sequoia"),
    (19000, 19999, "macOS 26 Tahoe"),  # verified: model 19607 on macOS 26.7.2
)
# Oldest release the scripts are tested against.
OLDEST_SUPPORTED_MODEL_VERSION = 16000


def macos_for_model_version(version: int | None) -> str | None:
    if version is None:
        return None
    return next((name for low, high, name in MODEL_VERSION_RANGES if low <= version <= high), None)


def describe(name: str) -> str:
    table, candidates = resolve(name)
    return f"{table}.{'/'.join(candidates)}"


class Degradation:
    """Collects the ``degraded`` entries a result reports for optional columns it had to do without."""

    def __init__(self, schema: SchemaRegistry):
        self._schema = schema
        self._missing: dict[str, list[str]] = {}
        self._notes: dict[str, str] = {}

    def check(self, section: str, *names: str) -> bool:
        """True when every column is present; otherwise record *section* as degraded and return False."""
        missing = self._schema.missing(*names)
        if missing:
            recorded = self._missing.setdefault(section, [])
            recorded.extend(column for column in missing if column not in recorded)
        return not missing

    def note(self, section: str, reason: str) -> None:
        """Record *section* as degraded for a reason other than a missing column."""
        self._notes.setdefault(section, reason)

    @property
    def entries(self) -> list[dict[str, str]]:
        return [
            {"section": section, "reason": f"missing column(s): {', '.join(columns)}"}
            for section, columns in self._missing.items()
        ] + [{"section": section, "reason": reason} for section, reason in self._notes.items()]


def album_junction(schema: SchemaRegistry) -> tuple[str, str, str] | None:
    """(table, album column, asset column) of the album↔asset join table, or None.

    Core Data numbers it per schema version (Z_26ASSETS, Z_27ASSETS, Z_28ASSETS, …),
    so it is found by shape rather than by name.
    """
    for table in schema.tables():
        if not (table.startswith("Z_") and "ASSETS" in table.upper()):
            continue
        album_col = asset_col = None
        for column in sorted(schema.columns(table)):
            if "ALBUMS" in column.upper():
                album_col = column
            elif "ASSETS" in column.upper():
                asset_col = column
        if album_col and asset_col:
            return table, album_col, asset_col
    return None


class PhotosConnection(sqlite3.Connection):
    """Connection that caches its SchemaRegistry (plain connections can't hold attributes or weakrefs)."""

    schema_registry: SchemaRegistry | None = None
    db_file: str | None = None


def get_schema(conn_or_cursor: sqlite3.Connection | sqlite3.Cursor) -> SchemaRegistry:
    """The SchemaRegistry for a connection (or a cursor's connection), cached when possible."""
    conn = conn_or_cursor.connection if isinstance(conn_or_cursor, sqlite3.Cursor) else conn_or_cursor
    if not isinstance(conn, PhotosConnection):
        return SchemaRegistry(conn)
    if conn.schema_registry is None:
        conn.schema_registry = SchemaRegistry(conn)
    return conn.schema_registry
