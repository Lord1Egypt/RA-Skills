# -*- coding: utf-8 -*-

import requests

OLD_BASE_URL = (
    "https://api.euskadi.eus/appcont/meteorologia/meteodat/images/{number:02}.png"
)
MODERN_BASE_URL = "https://www.euskalmet.euskadi.eus/media/assets/icons/euskalmet/webmet00-i{number:02}d.svg"


def download_old():
    for number in range(53):
        res = requests.get(OLD_BASE_URL.format(number=number))
        with open(f"images/{number:02}.png", "wb") as fp:

            fp.write(res.content)


def download_modern():
    for number in range(53):
        res = requests.get(MODERN_BASE_URL.format(number=number))
        with open(f"images-modern/webmet00-i{number:02}d.svg", "wb") as fp:

            fp.write(res.content)


if __name__ == "__main__":
    download_old()
    download_modern()
