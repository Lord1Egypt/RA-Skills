#!/usr/bin/env bash
# scripts/survey_arxiv.sh
# Usage: ./survey_arxiv.sh <year> <theme>
# Example: ./survey_arxiv.sh 2026 "AI assisted open source contribution"

set -e

YEAR=$1
THEME=$2
OUTPUT_DIR="${3:-.}"

if [ -z "$YEAR" ] || [ -z "$THEME" ]; then
    echo "Usage: $0 <year> <theme> [output_dir]"
    echo "Example: $0 2026 \"RAG retrieval augmented generation\""
    exit 1
fi

# Generate slug from theme (English only, no Chinese chars)
THEME_SLUG=$(echo "$THEME" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null || echo "$THEME" | tr ' ' '-' | tr -cd 'a-zA-Z0-9-')
THEME_SLUG=$(echo "$THEME_SLUG" | tr ' ' '-' | sed 's/--*/-/g' | tr '[:upper:]' '[:lower:]' | cut -c1-50)

OUTPUT_FILE="$OUTPUT_DIR/arxiv-survey-${YEAR}-${THEME_SLUG}.md"

echo "🔍 Searching arXiv for papers from $YEAR on: $THEME"
echo "📁 Output: $OUTPUT_FILE"

# Calculate start date (January 1st of the given year)
START_DATE="${YEAR}0101"
END_DATE=$(date +%Y%m%d)

# Build search query - convert Chinese to English keywords if needed
SEARCH_QUERY=$(echo "$THEME" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null || echo "$THEME")
SEARCH_QUERY=$(echo "$SEARCH_QUERY" | tr ' ' '+')

# Query arXiv API for up to 50 papers
MAX_RESULTS=50
ARXIV_URL="https://export.arxiv.org/api/query?search_query=all:${SEARCH_QUERY}&start=0&max_results=${MAX_RESULTS}&sortBy=submittedDate&sortOrder=descending"

echo "📡 Querying: $ARXIV_URL"

# Fetch results
RESPONSE=$(curl -sL "$ARXIV_URL")

# Parse XML and extract paper information
# This is a simplified parser - in production, use proper XML parsing
echo "$RESPONSE" | grep -oP '<entry>.*?</entry>' | head -20 | while read -r entry; do
    TITLE=$(echo "$entry" | grep -oP '<title[^>]*>\K[^<]+' | head -1 | xargs)
    SUMMARY=$(echo "$entry" | grep -oP '<summary[^>]*>\K[^<]+' | head -1 | xargs)
    AUTHORS=$(echo "$entry" | grep -oP '<name>\K[^<]+' | tr '\n' ', ' | sed 's/,$//')
    ID=$(echo "$entry" | grep -oP '<id>\K[^<]+' | head -1)
    PUBLISHED=$(echo "$entry" | grep -oP '<published>\K[^<]+' | head -1 | cut -d'T' -f1)
    
    # Filter by year
    PAPER_YEAR=$(echo "$PUBLISHED" | cut -d'-' -f1)
    if [ "$PAPER_YEAR" -ge "$YEAR" ] 2>/dev/null; then
        echo "✅ Found: $TITLE ($PUBLISHED)"
    fi
done

echo ""
echo "📝 Generating report: $OUTPUT_FILE"

# Generate markdown report
cat > "$OUTPUT_FILE" << EOF
# ArXiv Survey: $THEME ($YEAR-Present)

> Generated on $(date +%Y-%m-%d)  
> Theme: $THEME  
> Year Range: $YEAR to Present

## Table of Contents

*Categories and papers will be auto-generated based on search results*

---

## Detailed Papers

*Paper details with Chinese abstracts will be listed here*

---

## Search Info

- **Query**: $THEME
- **Year Range**: $YEAR to $(date +%Y)
- **Source**: arXiv API
- **Generated**: $(date)
EOF

echo "✅ Report generated: $OUTPUT_FILE"
echo ""
echo "📊 Next steps:"
echo "   1. Review the generated report"
echo "   2. Categories and translations will be refined by the agent"
echo "   3. Additional papers can be fetched if needed"
