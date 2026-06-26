import argparse
from freesound_config import load_config, save_config, DEFAULT_REDIRECT_URI, CONFIG_PATH


def main() -> None:
    parser = argparse.ArgumentParser(description="Save Freesound OAuth app credentials locally.")
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    parser.add_argument("--redirect-uri", default=DEFAULT_REDIRECT_URI)
    args = parser.parse_args()

    data = load_config()
    data.update(
        {
            "client_id": args.client_id,
            "client_secret": args.client_secret,
            "redirect_uri": args.redirect_uri,
        }
    )
    save_config(data)
    print(f"Saved credentials to {CONFIG_PATH}")


if __name__ == "__main__":
    main()
