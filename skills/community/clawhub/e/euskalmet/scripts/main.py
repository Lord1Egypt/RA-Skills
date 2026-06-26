# -*- coding: utf-8 -*-
from copy import deepcopy
import json
import jwt
import requests
import time
import datetime
import os
import argparse
import sys
from dotenv import load_dotenv


BASE_URL = "https://api.euskadi.eus/"

location_url = (
    "euskalmet/weather/regions/basque_country/zones/{zone}/locations/{location}"
)
forecast_url = "/forecast/trends/at/{year}/{month:02}/{day:02}/for/{forecastday}"

region_zones = "euskalmet/geo/regions/{region}/zones"
zone_locations = "euskalmet/geo/regions/{region}/zones/{zone}/locations"


def load_file(filename):
    with open(filename, "r") as fp:
        return fp.read()


def process_results(input):
    output = deepcopy(input)
    trendsByDate = []
    for item in output.get("trendsByDate", {}).get("set", []):
        id = item.get("weather", {}).get("id", "")
        item["weather"]["icon_name"] = f"{id}.png"
        item["weather"][
            "full_path"
        ] = f"https://api.euskadi.eus/{item.get('weather', {}).get('path', '')}"
        item["weather"]["icon_name_modern"] = f"webmet00-i{id}d.svg"
        item["weather"][
            "full_path_modern"
        ] = f"https://www.euskalmet.euskadi.eus/media/assets/icons/euskalmet/webmet00-i{id}d.svg"
        trendsByDate.append(item)
    output["trendsByDate"] = trendsByDate

    return output


def download_locations(region="basque_country"):
    """request all available zones and cities from a given region"""
    session = get_connection()

    response = session.get(f"{BASE_URL}{region_zones}".format(region=region))
    data = []
    if response.ok:
        for item in response.json():
            location_responses = session.get(
                f"{BASE_URL}{zone_locations}".format(
                    region=region, zone=item.get("regionZoneId")
                )
            )
            print(f'Downloading {region} {item["regionZoneId"]}')
            if location_responses.ok:
                for location in location_responses.json():
                    data.append(
                        {
                            "region": region,
                            "zone": item.get("regionZoneId"),
                            "location": location.get("regionZoneLocationId"),
                        }
                    )

    with open("available-locations.json", "w") as fp:
        json.dump(data, fp)

    return


def get_bearer_token():
    """get the authentication token to communicate with the API"""
    load_dotenv()
    email = os.environ.get("EUSKALMET_API_EMAIL")
    private_key = os.environ.get("EUSKALMET_API_PRIVATE_KEY")
    
    if not email or not private_key:
        print(f"DEBUG: EUSKALMET_API_EMAIL={email}")
        print(f"DEBUG: EUSKALMET_API_PRIVATE_KEY is {'set' if private_key else 'not set'}")

    assert bool(email)
    assert bool(private_key)

    # Ensure private key handles literal \n if stored as a single string in some environments
    if "\\n" in private_key:
        private_key = private_key.replace("\\n", "\n")

    claim_set = {
        "aud": "met01.apikey",
        "iss": "sampleApp",
        "exp": int(time.time() + (60 * 60)),
        "version": "1.0.0",
        "iat": int(time.time()),
        "email": email,
    }
    return jwt.encode(claim_set, private_key, algorithm="RS256")


def get_connection():
    bearer_token = get_bearer_token()
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {bearer_token}"})
    return session


def main():
    LOCATIONS_TO_PROCESS = json.loads(load_file("available-locations.json"))

    session = get_connection()

    today = datetime.datetime.now()
    year = today.year
    month_str = f"{today.month:02}"
    day_str = f"{today.day:02}"

    forecastday = f"{year}{month_str}{day_str}"

    for item in LOCATIONS_TO_PROCESS:
        assert "zone" in item
        assert "location" in item

        url = f"{BASE_URL}{location_url}{forecast_url}".format(
            year=year,
            month=int(month_str),
            day=int(day_str),
            forecastday=forecastday,
            zone=item["zone"],
            location=item["location"],
        )
        print(f"Downloading forecast: {item['location']} {forecastday} ")

        try:
            result = session.get(url, timeout=10) # 10 segunduko timeout-a
            result.raise_for_status()  # HTTP errorea badago, salbuespena botako du

            results_json = result.json()
            processed_results = process_results(results_json)

            # Get the icon for today
            today_iso = f"{year}-{month_str}-{day_str}"
            today_icon_id = None
            for trend in processed_results.get("trendsByDate", []):
                if trend.get("date", "").startswith(today_iso):
                    today_icon_id = trend.get("weather", {}).get("id")
                    break
            if not today_icon_id and processed_results.get("trendsByDate"):
                    today_icon_id = processed_results["trendsByDate"][0]["weather"]["id"]

            if today_icon_id:
                processed_results["today_icon_local"] = os.path.abspath(f"images-modern/webmet00-i{today_icon_id}d.svg")

            with open(f'forecasts/{item["location"]}-euskalmet.json', "w") as fp:
                json.dump(processed_results, fp)

        except requests.exceptions.RequestException as e:
            print(f"Errorea Euskalmet-ekin konektatzean: {e}", file=sys.stderr)
            sys.exit(1)


def print_locations():
    """print all available locations"""
    LOCATIONS_TO_PROCESS = json.loads(load_file("available-locations.json"))
    print("ZONE                            LOCATION")
    for item in LOCATIONS_TO_PROCESS:
        print(f"{item['zone']: <20}            {item['location']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Euskalmet downloader",
        description="Download weather forecast for coming days from Euskalmet API",
    )
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download the list of available locations and store in a JSON file",
    )
    parser.add_argument(
        "-l", "--locations", action="store_true", help="List all available locations"
    )

    args = parser.parse_args()

    if args.download:
        download_locations()

    if args.locations:
        print_locations()

    if not args.download and not args.locations:
        # Update forecast only when no options are entered
        main()
