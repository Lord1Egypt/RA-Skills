import argparse
import json

from api_utils import get_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch Freesound sound details by ID.")
    parser.add_argument("sound_id", type=int)
    args = parser.parse_args()

    data = get_json(
        f"/sounds/{args.sound_id}/",
        {
            "fields": "id,name,username,license,duration,url,description,tags,type,filesize,bitrate,bitdepth,samplerate,channels,created,download,previews,images,num_downloads,avg_rating,num_ratings"
        },
    )
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
