#!/usr/bin/env python3
"""Validate assembly for interference, clearance, swept-volume collisions. All in subprocess.

Script must define:
  parts = {"name": solid, ...}
  sweeps = [{"name", "axis_origin", "axis_direction", "angle_start", "angle_end", "angle_step"}, ...]  # optional
"""

import argparse
from helpers import run_sandboxed, output_json, WORKSPACE


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--script", required=True)
    p.add_argument("--mode", choices=["static", "clearance", "sweep", "full"], default="full")
    p.add_argument("--min-clearance", type=float, default=1.0)
    args = p.parse_args()

    sandbox_script = f'''
import json, os, math, itertools, traceback

# --- user script ---
{args.script}
# --- end user script ---

_rp = os.environ["_RESULT_PATH"]
_ws = os.environ.get("_WORKSPACE", ".")
_mode = {repr(args.mode)}
_min_clearance = {args.min_clearance}


def _get_part(ctx):
    if hasattr(ctx, "part"): return ctx.part
    if hasattr(ctx, "sketch"): return ctx.sketch
    return ctx


try:
    if "parts" not in dir() and "parts" not in globals():
        raise ValueError("Script must define `parts = {{'name': part, ...}}` dict.")

    _parts = {{k: _get_part(v) for k, v in parts.items()}}
    _sweeps = globals().get("sweeps", [])

    _result = {{
        "success": True,
        "part_count": len(_parts),
        "parts": list(_parts.keys()),
    }}

    # --- static interference ---
    if _mode in ("static", "full"):
        _interferences = []
        for (na, pa), (nb, pb) in itertools.combinations(_parts.items(), 2):
            try:
                _ix = pa & pb
                _vol = _ix.volume if hasattr(_ix, "volume") else 0.0
                if _vol > 0.01:
                    _bb = _ix.bounding_box()
                    _interferences.append({{
                        "part_a": na, "part_b": nb,
                        "overlap_volume_mm3": round(_vol, 3),
                        "overlap_center_mm": {{"x": round(_bb.center().X, 2), "y": round(_bb.center().Y, 2), "z": round(_bb.center().Z, 2)}},
                    }})
            except Exception as e:
                _interferences.append({{"part_a": na, "part_b": nb, "error": str(e)}})
        _result["static_interference"] = {{
            "checked_pairs": len(list(itertools.combinations(_parts, 2))),
            "interferences_found": len([i for i in _interferences if "overlap_volume_mm3" in i]),
            "details": _interferences,
        }}

    # --- clearance ---
    if _mode in ("clearance", "full"):
        _clearances = []
        for (na, pa), (nb, pb) in itertools.combinations(_parts.items(), 2):
            try:
                _bba = pa.bounding_box()
                _bbb = pb.bounding_box()
                def _gap(a0, a1, b0, b1):
                    if a1 < b0: return b0 - a1
                    if b1 < a0: return a0 - b1
                    return 0.0
                _gx = _gap(_bba.min.X, _bba.max.X, _bbb.min.X, _bbb.max.X)
                _gy = _gap(_bba.min.Y, _bba.max.Y, _bbb.min.Y, _bbb.max.Y)
                _gz = _gap(_bba.min.Z, _bba.max.Z, _bbb.min.Z, _bbb.max.Z)
                _mc = math.sqrt(_gx**2 + _gy**2 + _gz**2) if (_gx or _gy or _gz) else 0.0
                _clearances.append({{"part_a": na, "part_b": nb, "min_clearance_mm": round(_mc, 3)}})
            except Exception as e:
                _clearances.append({{"part_a": na, "part_b": nb, "error": str(e)}})
        _result["clearance"] = {{
            "min_acceptable_mm": _min_clearance,
            "violations": len([c for c in _clearances if c.get("min_clearance_mm", 999) < _min_clearance and "error" not in c]),
            "details": _clearances,
        }}

    # --- swept volume ---
    if _mode in ("sweep", "full") and _sweeps:
        from build123d import Axis, Vector, export_step

        _collisions = []
        for _sw in _sweeps:
            _sn = _sw["name"]
            if _sn not in _parts:
                _collisions.append({{"sweep": _sn, "error": f"Part '{{_sn}}' not in parts."}})
                continue
            _mp = _parts[_sn]
            _origin = Vector(*_sw["axis_origin"])
            _dir = Vector(*_sw["axis_direction"])
            _a0 = _sw.get("angle_start", -45)
            _a1 = _sw.get("angle_end", 45)
            _step = _sw.get("angle_step", 5)
            _statics = {{k: v for k, v in _parts.items() if k != _sn}}

            _swept = None
            _n_angles = 0
            _a = _a0
            while _a <= _a1:
                try:
                    _rot = _mp.rotate(Axis(_origin, _dir), _a)
                    _swept = _rot if _swept is None else (_swept + _rot)
                    _n_angles += 1
                except: pass
                _a += _step

            if _swept is None:
                _collisions.append({{"sweep": _sn, "error": "No valid poses."}})
                continue

            try:
                _sp = os.path.join(_ws, f"swept_{{_sn}}.step")
                os.makedirs(os.path.dirname(_sp), exist_ok=True)
                export_step(_swept, _sp)
            except: pass

            _found = False
            for _sk, _sv in _statics.items():
                try:
                    _ix = _swept & _sv
                    _vol = _ix.volume if hasattr(_ix, "volume") else 0.0
                    if _vol > 0.01:
                        _found = True
                        _bb = _ix.bounding_box()
                        _collisions.append({{
                            "sweep": _sn, "collides_with": _sk,
                            "overlap_volume_mm3": round(_vol, 3),
                            "overlap_center_mm": {{"x": round(_bb.center().X, 2), "y": round(_bb.center().Y, 2), "z": round(_bb.center().Z, 2)}},
                            "angles_checked": _n_angles,
                        }})
                except Exception as e:
                    _collisions.append({{"sweep": _sn, "collides_with": _sk, "error": str(e)}})

            if not _found:
                _collisions.append({{"sweep": _sn, "collides_with": None, "status": "clear", "angles_checked": _n_angles}})

        _result["swept_volume"] = {{
            "sweeps_defined": len(_sweeps),
            "collisions_found": len([c for c in _collisions if c.get("overlap_volume_mm3", 0) > 0]),
            "details": _collisions,
        }}

    # --- verdict ---
    _has_ix = any(i.get("overlap_volume_mm3", 0) > 0 for i in _result.get("static_interference", {{}}).get("details", []))
    _has_sw = any(c.get("overlap_volume_mm3", 0) > 0 for c in _result.get("swept_volume", {{}}).get("details", []))
    _has_cl = _result.get("clearance", {{}}).get("violations", 0) > 0

    if _has_ix or _has_sw:
        _result["verdict"] = "FAIL"
        _reasons = []
        if _has_ix: _reasons.append("Static interference detected.")
        if _has_sw: _reasons.append("Swept volume collision detected.")
        if _has_cl: _reasons.append(f"Clearance below {{_min_clearance}}mm.")
        _result["verdict_reason"] = _reasons
    elif _has_cl:
        _result["verdict"] = "WARN"
        _result["verdict_reason"] = [f"Clearance below {{_min_clearance}}mm."]
    else:
        _result["verdict"] = "PASS"
        _result["verdict_reason"] = ["No interference, clearance OK."]

    with open(_rp, "w") as f:
        json.dump(_result, f)

except Exception:
    with open(_rp, "w") as f:
        json.dump({{"success": False, "error": traceback.format_exc()[-2000:]}}, f)
'''

    output_json(run_sandboxed(sandbox_script, timeout=180))  # longer timeout for swept volumes


if __name__ == "__main__":
    main()
