import replicate
import urllib.request
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--aspect-ratio", default="1:1")
    parser.add_argument("--output", default="generated_image.png")
    args = parser.parse_args()

    output = replicate.run(
        "google/nano-banana-pro",
        input={
            "prompt": args.prompt,
            "aspect_ratio": args.aspect_ratio,
            "output_format": "png",
            "safety_filter_level": "block_only_high",
        },
    )

    # Replicate returns a FileOutput; download the image
    url = str(output[0]) if isinstance(output, list) else str(output)
    urllib.request.urlretrieve(url, args.output)
    print(f"Image saved to {args.output}")

if __name__ == "__main__":
    main()
