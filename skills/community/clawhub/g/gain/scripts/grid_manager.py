"""
Find the nearest supported grid point given latitude/longitude.
Uses Haversine distance to match against 7 built-in locations.
"""
import json
import math
import os


def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def load_grid_points(base_dir):
    path = os.path.join(base_dir, "data", "grid_points.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["locations"]


def find_nearest_location(lat, lon, base_dir):
    """Return (location_dict, distance_km) for the nearest supported grid point."""
    locations = load_grid_points(base_dir)
    best, best_dist = None, float("inf")
    for loc in locations:
        d = _haversine_km(lat, lon, loc["lat"], loc["lon"])
        if d < best_dist:
            best, best_dist = loc, d
    return best, round(best_dist, 1)


def list_locations(base_dir):
    """Return all supported locations as a formatted list."""
    locations = load_grid_points(base_dir)
    return [
        {"code": l["code"], "name": l["name"], "name_en": l["name_en"],
         "lat": l["lat"], "lon": l["lon"]}
        for l in locations
    ]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python grid_manager.py <base_dir> <lat> <lon>")
        sys.exit(1)
    base = sys.argv[1]
    lat, lon = float(sys.argv[2]), float(sys.argv[3])
    loc, dist = find_nearest_location(lat, lon, base)
    print(f"Nearest: {loc['name']} ({loc['code']}), "
          f"lat={loc['lat']}, lon={loc['lon']}, distance={dist} km")
