#!/usr/bin/env bash
# Generate an adaptive learning course from a questions.json file
# Usage: ./generate-course.sh <course-id> <questions-json> <output-dir>
#
# This script takes a questions.json and bundles it with the framework
# into a self-contained directory that can be opened in a browser.

set -euo pipefail

COURSE_ID="${1:?Usage: $0 <course-id> <questions.json> <output-dir>}"
QUESTIONS="${2:?Provide path to questions.json}"
OUTPUT="${3:?Provide output directory}"

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FRAMEWORK="$SKILL_DIR/assets/framework"

mkdir -p "$OUTPUT"

# Copy framework
cp "$FRAMEWORK/index.html" "$OUTPUT/"
cp "$FRAMEWORK/style.css" "$OUTPUT/"
cp "$FRAMEWORK/engine.js" "$OUTPUT/"
cp "$FRAMEWORK/ts-fsrs.umd.js" "$OUTPUT/"

# Generate preload script with inline questions
QDATA=$(cat "$QUESTIONS")
cat > "$OUTPUT/preload-${COURSE_ID}.js" <<PRELOAD_EOF
(function() {
  var KEY = 'alearn_${COURSE_ID}_questions';
  if (localStorage.getItem(KEY)) return;
  var questions = ${QDATA};
  localStorage.setItem(KEY, JSON.stringify(questions));
  console.log('${COURSE_ID} questions pre-loaded:', questions.length);
})();
PRELOAD_EOF

# Add preload script to index.html (before engine.js)
sed -i "s|<script src=\"engine.js\"></script>|<script src=\"preload-${COURSE_ID}.js\"></script>\n<script src=\"engine.js\"></script>|" "$OUTPUT/index.html"

# Remove any other preload scripts from index.html
sed -i "/preload-.*\.js/!b; /preload-${COURSE_ID}\.js/b; d" "$OUTPUT/index.html"

echo "✅ Course '${COURSE_ID}' generated at: $OUTPUT"
echo "   Open index.html in a browser to start learning."
