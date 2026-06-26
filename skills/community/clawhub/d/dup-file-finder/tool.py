import argparse
import os
import hashlib

def calculate_checksum(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def find_duplicates(directory):
    hashes = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filename = os.path.join(root, file)
            file_hash = calculate_checksum(filename)
            if file_hash in hashes:
                hashes[file_hash].append(filename)
            else:
                hashes[file_hash] = [filename]
    return {k: v for k, v in hashes.items() if len(v) > 1}

def main():
    parser = argparse.ArgumentParser(description='Find duplicate files in a directory')
    parser.add_argument('directory', help='the directory to search for duplicates')
    args = parser.parse_args()
    duplicates = find_duplicates(args.directory)
    for file_hash, files in duplicates.items():
        print(f"Duplicate files (hash: {file_hash}):")
        for file in files:
            print(f"- {file}")
        print()

if __name__ == "__main__":
    main()
