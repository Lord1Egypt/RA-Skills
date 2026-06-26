#!/bin/bash

set -ueo pipefail

# Audio file renamer - converts Chinese/special char filenames to pure English
# Usage: 
#   ./audio-rename.sh <file_path>              # rename to video_audio.m4a
#   ./audio-rename.sh <file_path> <new_name>   # rename to <new_name>.m4a
#   ./audio-rename.sh <dir_path> --all         # batch rename all m4a files

if [ $# -lt 1 ]; then
    echo "Usage: $0 <file_path> [new_name]"
    echo "       $0 <dir_path> --all"
    exit 1
fi

input="$1"
output_name="${2:-video_audio}"

# Check if --all flag for batch mode
if [ "${2:-}" = "--all" ]; then
    # Batch mode
    if [ ! -d "$input" ]; then
        echo "❌ Error: '$input' is not a directory"
        exit 1
    fi
    
    counter=1
    for file in "$input"/*.m4a "$input"/*.mp3 "$input"/*.wav "$input"/*.flac; do
        [ -e "$file" ] || continue
        
        filename=$(basename "$file")
        ext="${filename##*.}"
        new_name=$(printf "audio_%03d.%s" $counter $ext)
        
        # Skip if already named correctly
        if [ "$filename" = "$new_name" ]; then
            ((counter++))
            continue
        fi
        
        # Handle name conflicts
        target="$input/$new_name"
        while [ -e "$target" ]; do
            ((counter++))
            new_name=$(printf "audio_%03d.%s" $counter $ext)
            target="$input/$new_name"
        done
        
        mv "$file" "$target"
        echo "✅ $filename → $new_name"
        ((counter++))
    done
    echo "✅ Batch rename complete!"
    exit 0
fi

# Single file mode
if [ ! -f "$input" ]; then
    echo "❌ Error: File '$input' not found"
    exit 1
fi

# Get directory and extension
dir=$(dirname "$input")
filename=$(basename "$input")
ext="${filename##*.}"

# Generate output filename
output_file="$dir/${output_name}.${ext}"

# Handle name conflicts
if [ -e "$output_file" ]; then
    counter=1
    while [ -e "$dir/${output_name}_${counter}.${ext}" ]; do
        ((counter++))
    done
    output_file="$dir/${output_name}_${counter}.${ext}"
fi

# Rename
mv "$input" "$output_file"
echo "✅ Renamed: $filename → $(basename "$output_file")"
echo "📁 Location: $output_file"
