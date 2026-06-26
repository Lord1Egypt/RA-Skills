#!/bin/bash
# Analyze merge conflicts - only shows conflicted sections with context

set -e

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository"
    exit 1
fi

if ! git diff --name-only --diff-filter=U | grep -q .; then
    echo "No merge conflicts detected"
    exit 0
fi

echo "=== Detailed Conflict Analysis ==="
echo ""

# Get merge/rebase info
if [ -f .git/MERGE_HEAD ]; then
    MERGE_TYPE="merge"
    THEIR_BRANCH=$(git name-rev --name-only MERGE_HEAD)
    echo "Operation: Merge from $THEIR_BRANCH"
elif [ -d .git/rebase-merge ] || [ -d .git/rebase-apply ]; then
    MERGE_TYPE="rebase"
    if [ -f .git/rebase-merge/head-name ]; then
        THEIR_BRANCH=$(cat .git/rebase-merge/head-name | sed 's|refs/heads/||')
    else
        THEIR_BRANCH="(unknown)"
    fi
    echo "Operation: Rebase onto $THEIR_BRANCH"
else
    MERGE_TYPE="unknown"
    THEIR_BRANCH="(unknown)"
fi

OUR_BRANCH=$(git branch --show-current)
if [ -z "$OUR_BRANCH" ]; then
    OUR_BRANCH="(detached HEAD at $(git rev-parse --short HEAD))"
fi
echo "Current branch: $OUR_BRANCH"
echo ""

# Check for submodule conflicts
SUBMODULE_CONFLICTS=$(git diff --name-only --diff-filter=U | while read file; do
    if git config -f .gitmodules "submodule.$file.path" >/dev/null 2>&1; then
        echo "$file"
    fi
done)

if [ -n "$SUBMODULE_CONFLICTS" ]; then
    echo "⚠️  Submodule conflicts detected!"
    echo "Conflicted submodules: $SUBMODULE_CONFLICTS"
    echo "See conflict-resolution.md for submodule handling"
    echo ""
fi

TOTAL_FILES=$(git diff --name-only --diff-filter=U | wc -l)
echo "Total conflicted files: $TOTAL_FILES"
echo ""

# Function to extract only conflict sections with context
extract_conflict_sections() {
    local file="$1"
    local context_lines=5
    
    # Use awk to extract conflict sections with context
    awk -v context=$context_lines '
    BEGIN { 
        in_conflict = 0
        conflict_num = 0
        buffer_size = 0
    }
    
    # Start of conflict
    /^<<<<<<< / {
        conflict_num++
        in_conflict = 1
        print ""
        print "--- Conflict #" conflict_num " (line " NR ") ---"
        # Print buffered context
        for (i = 0; i < buffer_size; i++) {
            print buffer[i]
        }
        buffer_size = 0
        print $0
        next
    }
    
    # End of conflict
    /^>>>>>>> / {
        print $0
        # Print context after
        for (i = 1; i <= context; i++) {
            if (getline > 0) {
                print $0
            }
        }
        print ""
        in_conflict = 0
        next
    }
    
    # Inside conflict
    in_conflict == 1 {
        print $0
        next
    }
    
    # Outside conflict - maintain rolling buffer
    {
        buffer[buffer_size % context] = $0
        buffer_size++
        if (buffer_size > context) buffer_size = context
    }
    ' "$file"
}

# Analyze each conflicted file
FILE_COUNT=0
for file in $(git diff --name-only --diff-filter=U); do
    FILE_COUNT=$((FILE_COUNT + 1))
    
    if [ $FILE_COUNT -gt 10 ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "... and $((TOTAL_FILES - 10)) more conflicted files"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        break
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📄 File: $file"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    CONFLICT_COUNT=$(grep -c "^<<<<<<< " "$file" 2>/dev/null || echo "0")
    FILE_SIZE=$(wc -l < "$file" 2>/dev/null || echo "0")
    echo "Conflicts: $CONFLICT_COUNT sections | File size: $FILE_SIZE lines"
    
    echo ""
    echo "=== Conflict Sections Only (with 5 lines context) ==="
    extract_conflict_sections "$file"
    
    echo ""
    echo "=== For Full Context ==="
    echo "Base:   git show :1:$file"
    echo "Ours:   git show :2:$file"
    echo "Theirs: git show :3:$file"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Review each conflict section"
echo "2. Understand intent of both changes"
echo "3. Decide: merge both, keep one, or ask user"
echo "4. Edit files to resolve"
echo "5. git add <file> when resolved"
echo "6. git $MERGE_TYPE --continue"

