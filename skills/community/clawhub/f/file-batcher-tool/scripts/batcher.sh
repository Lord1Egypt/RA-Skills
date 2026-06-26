#!/bin/bash
# File Batcher - Batch file operations
# Version: 1.0.0

# Rename files with pattern
batch_rename() {
    local folder="$1"
    local pattern="$2"
    local count=0
    
    if [ ! -d "$folder" ]; then
        echo "❌ Folder not found: $folder"
        return 1
    fi
    
    cd "$folder" || return 1
    
    case "$pattern" in
        prefix_*)
            local prefix="${pattern%_*}"
            for file in *; do
                [ -f "$file" ] && mv "$file" "${prefix}_$file" && ((count++))
            done
            ;;
        *_suffix)
            local suffix="${pattern#*_}"
            for file in *; do
                if [ -f "$file" ]; then
                    local name="${file%.*}"
                    local ext="${file##*.}"
                    [ "$name" != "$ext" ] && mv "$file" "${name}_${suffix}.${ext}" || mv "$file" "${file}_${suffix}"
                    ((count++))
                fi
            done
            ;;
        *###*)
            local prefix="${pattern%###}"
            local num=1
            for file in *; do
                [ -f "$file" ] && mv "$file" "${prefix}$(printf '%03d' $num)" && ((num++)) && ((count++))
            done
            ;;
        lowercase)
            for file in *; do
                [ -f "$file" ] && mv "$file" "$(echo "$file" | tr '[:upper:]' '[:lower:]')" && ((count++))
            done
            ;;
        uppercase)
            for file in *; do
                [ -f "$file" ] && mv "$file" "$(echo "$file" | tr '[:lower:]' '[:upper:]')" && ((count++))
            done
            ;;
    esac
    
    echo "✅ Renamed $count files in $folder"
}

# Convert images
convert_images() {
    local folder="$1"
    local format="$2"
    local count=0
    
    if [ ! -d "$folder" ]; then
        echo "❌ Folder not found: $folder"
        return 1
    fi
    
    # Check for ImageMagick
    if ! command -v convert &> /dev/null; then
        echo "⚠️  ImageMagick not installed"
        echo "   Install: brew install imagemagick (Mac) or apt-get install imagemagick (Linux)"
        return 1
    fi
    
    cd "$folder" || return 1
    
    for file in *.jpg *.jpeg *.png *.gif *.webp 2>/dev/null; do
        [ -f "$file" ] && convert "$file" "${file%.*}.$format" && rm "$file" && ((count++))
    done
    
    echo "✅ Converted $count images to .$format"
}

# Organize files by type
organize_files() {
    local folder="$1"
    
    if [ ! -d "$folder" ]; then
        echo "❌ Folder not found: $folder"
        return 1
    fi
    
    cd "$folder" || return 1
    
    mkdir -p images documents videos audio archives
    
    # Images
    for ext in jpg jpeg png gif webp bmp svg; do
        mv *.$ext images/ 2>/dev/null
    done
    
    # Documents
    for ext in pdf doc docx xls xlsx ppt pptx txt md rtf; do
        mv *.$ext documents/ 2>/dev/null
    done
    
    # Videos
    for ext in mp4 avi mkv mov wmv flv; do
        mv *.$ext videos/ 2>/dev/null
    done
    
    # Audio
    for ext in mp3 wav flac aac ogg; do
        mv *.$ext audio/ 2>/dev/null
    done
    
    # Archives
    for ext in zip rar tar gz 7z; do
        mv *.$ext archives/ 2>/dev/null
    done
    
    echo "✅ Organized files in $folder"
    echo "   images/: $(ls images | wc -l | tr -d ' ') files"
    echo "   documents/: $(ls documents | wc -l | tr -d ' ') files"
    echo "   videos/: $(ls videos | wc -l | tr -d ' ') files"
    echo "   audio/: $(ls audio | wc -l | tr -d ' ') files"
    echo "   archives/: $(ls archives | wc -l | tr -d ' ') files"
}

# Find duplicates
find_duplicates() {
    local folder="$1"
    
    if [ ! -d "$folder" ]; then
        echo "❌ Folder not found: $folder"
        return 1
    fi
    
    echo "🔍 Finding duplicates in $folder..."
    echo ""
    
    cd "$folder" || return 1
    
    # Simple duplicate detection by size
    find . -type f -exec stat -f"%z %N" {} \; 2>/dev/null | sort -n | uniq -d -w 10 || \
    find . -type f -exec stat -c"%s %n" {} \; 2>/dev/null | sort -n | uniq -d -w 10
    
    echo ""
    echo "Tip: Use fdupes or dupeGuru for advanced duplicate detection"
}

# Count files
count_files() {
    local folder="$1"
    
    if [ ! -d "$folder" ]; then
        echo "❌ Folder not found: $folder"
        return 1
    fi
    
    local total=$(find "$folder" -type f | wc -l | tr -d ' ')
    local dirs=$(find "$folder" -type d | wc -l | tr -d ' ')
    
    echo "📊 $folder"
    echo "   Files: $total"
    echo "   Folders: $dirs"
}

# Find large files
find_large() {
    local folder="$1"
    local size="${2:-100M}"
    
    if [ ! -d "$folder" ]; then
        echo "❌ Folder not found: $folder"
        return 1
    fi
    
    echo "🔍 Files larger than $size in $folder:"
    echo ""
    
    find "$folder" -type f -size +$size -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' | sort -hr | head -20
}

# Show help
show_help() {
    echo "File Batcher - Batch file operations"
    echo ""
    echo "Usage:"
    echo "  batcher.sh rename \"<folder>\" \"<pattern>\""
    echo "  batcher.sh convert \"<folder>\" \"<format>\""
    echo "  batcher.sh organize \"<folder>\""
    echo "  batcher.sh duplicates \"<folder>\""
    echo "  batcher.sh count \"<folder>\""
    echo "  batcher.sh large \"<folder>\" [--size 100M]"
    echo ""
    echo "Rename Patterns:"
    echo "  prefix_*     - Add prefix to all files"
    echo "  *_suffix     - Add suffix to all files"
    echo "  name_###     - Sequential numbering"
    echo "  lowercase    - Convert to lowercase"
    echo "  uppercase    - Convert to uppercase"
}

# Main
case "$1" in
    rename)
        batch_rename "$2" "$3"
        ;;
    convert)
        convert_images "$2" "$3"
        ;;
    organize)
        organize_files "$2"
        ;;
    duplicates)
        find_duplicates "$2"
        ;;
    count)
        count_files "$2"
        ;;
    large)
        find_large "$2" "$3"
        ;;
    *)
        show_help
        ;;
esac
