import argparse
from pathlib import Path
import re


def split_into_batches(file_path, words_per_batch=3000, output_dir=None):
    input_path = Path(file_path)
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    text = input_path.read_text(encoding="utf-8")
    parts = re.split(r"(\s+)", text)

    batches = []
    current_batch = []
    current_word_count = 0

    for part in parts:
        current_batch.append(part)
        if not part.isspace():
            current_word_count += 1

        if current_word_count >= words_per_batch:
            batches.append("".join(current_batch))
            current_batch = []
            current_word_count = 0

    if current_batch:
        batches.append("".join(current_batch))

    batch_output_dir = Path(output_dir) if output_dir else input_path.parent / "batches"
    batch_output_dir.mkdir(parents=True, exist_ok=True)

    written_files = []
    for index, batch in enumerate(batches, start=1):
        batch_path = batch_output_dir / f"batch_{index}.txt"
        batch_path.write_text(batch, encoding="utf-8")
        written_files.append(batch_path)

    return written_files


def main():
    parser = argparse.ArgumentParser(description="Split a long text file into word-count-based batches.")
    parser.add_argument("file", help="Path to the source text file")
    parser.add_argument("words_per_batch", nargs="?", type=int, default=3000, help="Words per batch")
    parser.add_argument("--output-dir", help="Directory where batch files will be written")
    args = parser.parse_args()

    batch_files = split_into_batches(args.file, args.words_per_batch, output_dir=args.output_dir)
    for batch_file in batch_files:
        print(f"Created {batch_file}")


if __name__ == "__main__":
    main()