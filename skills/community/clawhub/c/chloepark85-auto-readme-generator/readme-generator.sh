#!/bin/bash

PROJECT_PATH=${1:-.}
PROJECT_NAME=$(basename "$PROJECT_PATH")

README_CONTENT="# $PROJECT_NAME\n\n## Description\n\nThis is a brief description of the project.\n\n## Installation\n\n\`\`\`bash\nnpm install\n# or\npip install -r requirements.txt\n\`\`\`\n\n## Usage\n\n\`\`\`bash\n# Example usage\n\`\`\`\n\n## License\n\nThis project is licensed under the MIT License.\n"

echo -e "$README_CONTENT" > "$PROJECT_PATH/README.md"
echo "README.md generated for $PROJECT_NAME in $PROJECT_PATH"
