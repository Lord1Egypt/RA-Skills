import argparse
from pathlib import Path
import re


def count_words(text):
    return len([word for word in re.split(r"\s+", text.strip()) if word])


def read_text(file_path):
    return Path(file_path).read_text(encoding="utf-8")


def get_file_word_count(file_path):
    path = Path(file_path)
    if not path.exists():
        return 0
    return count_words(read_text(path))


def compute_target_words(total_words, ratio=0.20):
    return round(total_words * ratio)


def estimate_batches(total_words, words_per_batch=20000):
    batch_count = (total_words + words_per_batch - 1) // words_per_batch
    return batch_count, words_per_batch


def aggregate_files(input_files, output_file, header=None):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_stream:
        if header:
            output_stream.write(header + "\n\n")

        for index, input_file in enumerate(input_files, start=1):
            input_path = Path(input_file)
            if not input_path.exists():
                continue

            output_stream.write(f"## Batch {index}\n\n")
            output_stream.write(input_path.read_text(encoding="utf-8"))
            output_stream.write("\n\n---\n\n")


def build_parser():
    parser = argparse.ArgumentParser(description="Utilities for long-form book summarization workflows.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    count_parser = subparsers.add_parser("count", help="Count words in a text file.")
    count_parser.add_argument("file", help="Path to the source text file")

    target_parser = subparsers.add_parser("target", help="Calculate target summary words from a source file.")
    target_parser.add_argument("file", help="Path to the source text file")
    target_parser.add_argument("--ratio", type=float, default=0.20, help="Target compression ratio")

    estimate_parser = subparsers.add_parser("estimate", help="Estimate number of batches for a word count.")
    estimate_parser.add_argument("words", type=int, help="Total word count")
    estimate_parser.add_argument("--batch-size", type=int, default=20000, help="Words per batch")

    aggregate_parser = subparsers.add_parser("aggregate", help="Aggregate batch files into a single markdown file.")
    aggregate_parser.add_argument("output", help="Output markdown path")
    aggregate_parser.add_argument("files", nargs="+", help="Input batch files in order")
    aggregate_parser.add_argument("--header", help="Optional markdown header")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "count":
        print(get_file_word_count(args.file))
        return

    if args.command == "target":
        total_words = get_file_word_count(args.file)
        target_words = compute_target_words(total_words, args.ratio)
        print(f"Source words: {total_words}")
        print(f"Target ratio: {args.ratio:.2f}")
        print(f"Target summary words: {target_words}")
        return

    if args.command == "estimate":
        batch_count, batch_size = estimate_batches(args.words, args.batch_size)
        print(f"Batches: {batch_count}")
        print(f"Words per batch: {batch_size}")
        return

    if args.command == "aggregate":
        aggregate_files(args.files, args.output, header=args.header)
        print(f"Aggregated into {args.output}")
        return


if __name__ == "__main__":
    main()