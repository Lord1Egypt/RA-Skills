#!/usr/bin/env python3
"""
Distance calculation utilities for film-location-scout skill.
Uses Haversine formula to calculate distances between GPS coordinates.
"""

import math
from typing import Tuple, List, Dict


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.

    Args:
        lat1: Latitude of point 1 in decimal degrees
        lon1: Longitude of point 1 in decimal degrees
        lat2: Latitude of point 2 in decimal degrees
        lon2: Longitude of point 2 in decimal degrees

    Returns:
        Distance in meters
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of Earth in meters
    r = 6371000

    return c * r


def format_distance(distance_meters: float) -> str:
    """
    Format distance for display.

    Args:
        distance_meters: Distance in meters

    Returns:
        Formatted string (e.g., "450m" or "1.2km")
    """
    if distance_meters < 1000:
        return f"{int(distance_meters)}m"
    else:
        return f"{distance_meters/1000:.1f}km"


def filter_locations_by_distance(
    user_lat: float,
    user_lon: float,
    locations: List[Dict],
    max_distance_km: float = 5.0
) -> List[Dict]:
    """
    Filter locations by distance from user position.

    Args:
        user_lat: User latitude
        user_lon: User longitude
        locations: List of location dicts with 'lat' and 'lon' keys
        max_distance_km: Maximum distance in kilometers

    Returns:
        List of locations within max_distance_km, sorted by distance
    """
    max_distance_m = max_distance_km * 1000

    locations_with_distance = []
    for loc in locations:
        distance = haversine_distance(
            user_lat, user_lon,
            loc['lat'], loc['lon']
        )
        if distance <= max_distance_m:
            loc_copy = loc.copy()
            loc_copy['distance_m'] = distance
            loc_copy['distance_formatted'] = format_distance(distance)
            locations_with_distance.append(loc_copy)

    # Sort by distance
    locations_with_distance.sort(key=lambda x: x['distance_m'])

    return locations_with_distance


def calculate_bounding_box(
    lat: float,
    lon: float,
    radius_km: float
) -> Tuple[float, float, float, float]:
    """
    Calculate bounding box for a given point and radius.

    Args:
        lat: Center latitude
        lon: Center longitude
        radius_km: Radius in kilometers

    Returns:
        Tuple of (min_lat, max_lat, min_lon, max_lon)
    """
    # Approximate degrees per km
    lat_degree_per_km = 1 / 111.32
    lon_degree_per_km = 1 / (111.32 * math.cos(math.radians(lat)))

    lat_delta = radius_km * lat_degree_per_km
    lon_delta = radius_km * lon_degree_per_km

    return (
        lat - lat_delta,  # min_lat
        lat + lat_delta,  # max_lat
        lon - lon_delta,  # min_lon
        lon + lon_delta   # max_lon
    )


def main():
    """CLI for testing distance calculations."""
    import sys

    if len(sys.argv) < 5:
        print("Usage: python3 distance_calc.py <lat1> <lon1> <lat2> <lon2>")
        print("Example: python3 distance_calc.py 31.2304 121.4737 31.2397 121.4997")
        sys.exit(1)

    lat1 = float(sys.argv[1])
    lon1 = float(sys.argv[2])
    lat2 = float(sys.argv[3])
    lon2 = float(sys.argv[4])

    distance = haversine_distance(lat1, lon1, lat2, lon2)
    print(f"Distance: {format_distance(distance)}")
    print(f"Exact: {distance:.2f} meters")


if __name__ == "__main__":
    main()
