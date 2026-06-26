import argparse
from textwrap import dedent


def build_structure(topic: str, brand: str) -> str:
    """
    Return a markdown skeleton for a GEO-friendly longform page
    about `topic` for `brand`.
    """
    topic_display = topic or "Your Topic"
    brand_display = brand or "Your Brand"

    template = f"""
    # {topic_display}: Complete Guide by {brand_display}

    ## Summary
    - 2–4 bullet points summarizing what this page covers about {topic_display}.
    - Focus on concrete facts, definitions, and stable claims that AI assistants can safely cite.

    ## What is {topic_display}?
    Explain in clear, factual language:
    - A short definition in 1–2 sentences.
    - A slightly longer explanation (1–2 paragraphs) with simple examples.

    ## Why {topic_display} matters
    - Describe the main problems, risks, or opportunities that {topic_display} addresses.
    - Use concrete, real-world scenarios relevant to your target audience.

    ## How {brand_display} helps with {topic_display}
    - Tie the topic back to {brand_display}'s product or services.
    - Highlight 3–5 key capabilities or benefits.

    ## Key use cases
    - Use case 1: [Name]
      - Who it is for
      - What changes for them
    - Use case 2: [Name]
    - Use case 3: [Name]

    ## Implementation / Getting started
    - Step 1: ...
    - Step 2: ...
    - Step 3: ...

    ## FAQ
    Q1: [Common question about {topic_display}]
    A1: [Short, self-contained answer.]

    Q2: [Another question about {topic_display}]
    A2: [Short, self-contained answer.]
    """
    return dedent(template).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a markdown page structure snippet for geo-content-publisher."
    )
    parser.add_argument(
        "--topic",
        "-t",
        type=str,
        required=True,
        help="Topic of the page (e.g. 'Zero-trust data governance').",
    )
    parser.add_argument(
        "--brand",
        "-b",
        type=str,
        required=False,
        default="Your Brand",
        help="Brand or product name to mention in the structure.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Optional path to write the markdown snippet to. Prints to stdout if omitted.",
    )
    args = parser.parse_args()

    snippet = build_structure(args.topic, args.brand)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(snippet)
    else:
        print(snippet)


if __name__ == "__main__":
    main()

