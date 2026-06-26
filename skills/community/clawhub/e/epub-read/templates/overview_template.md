# Overview Mode Output Template

# Book Overview

## Basic Information

- **Title**: {{ book_title }}
- **Author**: {{ author }}
- **Chapter Count**: {{ chapter_count }}
- **Total Word Count**: {{ total_words }}
- **XHTML File Count**: {{ total_xhtml_files }}
- **Estimated Reading Time**: {{ estimated_reading_time_minutes }} minutes
- **Output Directory**: {{ output_dir }}

## Table of Contents

{{ toc_structure }}

## Content Analysis

### Theme Overview

(Infer this from the title and TOC.)

### Complex Content Detection

{{ complex_content_report }}

## Recommended Next Steps

Depending on the user's goal, suggest one of the following:

- **Continue overview** - inspect more structural detail
- **Targeted reading** - read a specific chapter or chunk range with `targeted_read`
- **Full reading** - begin chunked sequential reading with `full_read`
- **Structured extraction** - extract keywords, concepts, quotes, or action items with `extract`
- **Complex content review** - inspect images, tables, and layout-heavy sections with `complex_content`
