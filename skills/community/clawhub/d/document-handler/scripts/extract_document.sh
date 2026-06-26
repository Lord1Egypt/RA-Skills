#!/bin/bash
# Extract text and metadata from any supported document format

set -e

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <file> [--metadata-only]"
    exit 1
fi

FILE="$1"
META_ONLY="${2:-}"

if [[ ! -f "$FILE" ]]; then
    echo "Error: File not found: $FILE" >&2
    exit 1
fi

EXT="${FILE##*.}"
EXT="${EXT,,}"  # lowercase

extract_metadata() {
    case "$EXT" in
        pdf)
            pdfinfo "$FILE" 2>/dev/null || echo "Could not extract PDF metadata"
            ;;
        docx|xlsx|pptx)
            echo "=== Office Document Metadata ==="
            unzip -p "$FILE" docProps/core.xml 2>/dev/null | sed 's/<[^>]*>/\n/g' | grep -v '^$' || echo "No metadata found"
            ;;
        odt|ods|odp)
            echo "=== OpenDocument Metadata ==="
            unzip -p "$FILE" meta.xml 2>/dev/null | sed 's/<[^>]*>/\n/g' | grep -v '^$' || echo "No metadata found"
            ;;
        epub)
            echo "=== EPUB Metadata ==="
            unzip -p "$FILE" "*.opf" 2>/dev/null | sed 's/<[^>]*>/\n/g' | grep -v '^$' | head -20 || echo "No metadata found"
            ;;
        rtf)
            echo "RTF metadata extraction not supported"
            ;;
        *)
            echo "Unknown format: $EXT"
            ;;
    esac
}

extract_text() {
    case "$EXT" in
        pdf)
            pdftotext -layout "$FILE" - 2>/dev/null || echo "Could not extract PDF text"
            ;;
        docx)
            unzip -p "$FILE" word/document.xml 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n' | sed 's/^ *//;s/ *$//' || echo "Could not extract DOCX text"
            ;;
        xlsx)
            echo "=== Excel Content ==="
            unzip -p "$FILE" xl/sharedStrings.xml 2>/dev/null | sed 's/<[^>]*>//g' | grep -v '^$' || echo "Could not extract XLSX text"
            ;;
        pptx)
            echo "=== PowerPoint Content ==="
            unzip -p "$FILE" ppt/slides/slide*.xml 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n' | grep -v '^$' || echo "Could not extract PPTX text"
            ;;
        odt)
            unzip -p "$FILE" content.xml 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n' || echo "Could not extract ODT text"
            ;;
        ods)
            unzip -p "$FILE" content.xml 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n' || echo "Could not extract ODS text"
            ;;
        odp)
            unzip -p "$FILE" content.xml 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n' || echo "Could not extract ODP text"
            ;;
        epub)
            # Find and extract HTML content
            for html in $(unzip -l "$FILE" | grep -E '\.(html|x?html)$' | awk '{print $4}' | head -20); do
                unzip -p "$FILE" "$html" 2>/dev/null | sed 's/<[^>]*>//g' | tr -s ' \n'
            done
            ;;
        rtf)
            textutil -convert txt -stdout "$FILE" 2>/dev/null || echo "Could not extract RTF text"
            ;;
        *)
            echo "Unknown format: $EXT"
            ;;
    esac
}

if [[ "$META_ONLY" == "--metadata-only" ]]; then
    extract_metadata
else
    echo "=== File: $FILE ==="
    echo ""
    extract_metadata
    echo ""
    echo "=== Content ==="
    extract_text
fi