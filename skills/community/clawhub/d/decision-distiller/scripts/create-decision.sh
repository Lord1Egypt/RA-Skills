#!/bin/bash
#
# create-decision.sh - Create a new decision record
# Usage: ./create-decision.sh "Decision title" [--template tech|process|strategy|quick]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${DECISION_DATA_DIR:-$SKILL_DIR/data}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse arguments
TITLE=""
TEMPLATE="standard"

while [[ $# -gt 0 ]]; do
    case $1 in
        --template)
            TEMPLATE="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            TITLE="$1"
            shift
            ;;
    esac
done

if [[ -z "$TITLE" ]]; then
    echo "Usage: $0 \"Decision title\" [--template tech|process|strategy|quick]"
    exit 1
fi

# Create data directory
mkdir -p "$DATA_DIR"

# Generate ID
DATE=$(date +%Y%m%d)
COUNTER=1
while [[ -f "$DATA_DIR/DEC-${DATE}-$(printf "%03d" $COUNTER).md" ]]; do
    COUNTER=$((COUNTER + 1))
done
DECISION_ID="DEC-${DATE}-$(printf "%03d" $COUNTER)"

# Generate dated filename
OUTPUT_FILE="$DATA_DIR/$DECISION_ID.md"

# Create decision record based on template
case $TEMPLATE in
    tech)
        cat > "$OUTPUT_FILE" << EOF
# Decision: $TITLE - $(date +%Y-%m-%d)

**ID**: $DECISION_ID
**Status**: pending
**Domain**: Technical
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Context
[What technical challenge or choice prompted this decision]

## Options

### Option 1: [Technology A]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Complexity**: Low/Medium/High

### Option 2: [Technology B]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Complexity**: Low/Medium/High

## Criteria
1. Performance - Weight: High
2. Maintainability - Weight: High
3. Team Familiarity - Weight: Medium

## Decision
**Chosen**: [TBD]

## Rationale
[TBD]

## Trade-offs
[TBD]

## Expected Outcome
[TBD]

## Actual Outcome
[TBD - fill in after implementation]

## Lessons Learned
[TBD - fill in after review]
EOF
        ;;
    process)
        cat > "$OUTPUT_FILE" << EOF
# Decision: $TITLE - $(date +%Y-%m-%d)

**ID**: $DECISION_ID
**Status**: pending
**Domain**: Process
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Context
[What workflow or process needs improvement]

## Current State
[How things work now]

## Options

### Option 1: [Approach A]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Implementation Effort**: 

### Option 2: [Approach B]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Implementation Effort**: 

## Stakeholders
- [Who is affected]

## Decision
**Chosen**: [TBD]

## Rollout Plan
1. [Step 1]
2. [Step 2]

## Success Metrics
[How to know if this worked]

## Expected Outcome
[TBD]

## Actual Outcome
[TBD - fill in after implementation]

## Lessons Learned
[TBD - fill in after review]
EOF
        ;;
    quick)
        cat > "$OUTPUT_FILE" << EOF
# Decision: $TITLE - $(date +%Y-%m-%d)

**ID**: $DECISION_ID
**Status**: pending
**Type**: Quick
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Context
[Brief description]

## Options
- A: [Description]
- B: [Description]

## Decision
**Chosen**: [TBD]

## Rationale
[One-line reasoning]

## Trade-offs
[Quick note on trade-offs]

## Expected Outcome
[TBD]

## Actual Outcome
[TBD]

## Lessons Learned
[TBD]
EOF
        ;;
    *)
        cat > "$OUTPUT_FILE" << EOF
# Decision: $TITLE - $(date +%Y-%m-%d)

**ID**: $DECISION_ID
**Status**: pending
**Created**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Context
[Description of the situation requiring a decision]

## Options Considered

### Option 1: [Name]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Estimated Impact**: 

### Option 2: [Name]
- **Description**: 
- **Pros**: 
- **Cons**: 
- **Estimated Impact**: 

## Decision Criteria
1. [Criterion 1] - Weight: High/Medium/Low
2. [Criterion 2] - Weight: High/Medium/Low

## Decision
**Chosen**: [TBD]

## Rationale
[Why this option was selected over others]

## Trade-offs
- **Accepted**: [What we gave up]
- **Mitigated**: [How we reduced risks]

## Expected Outcome
[What we expect to happen]

## Actual Outcome
[Filled in later - what actually happened]

## Lessons Learned
[Filled in later - insights from the outcome]

## Related Decisions
- [Link to related decision]
EOF
        ;;
esac

echo -e "${GREEN}✅ Decision record created: $DECISION_ID${NC}"
echo -e "${BLUE}📄 Location: $OUTPUT_FILE${NC}"
echo ""
echo "Next steps:"
echo "  1. Edit $OUTPUT_FILE"
echo "  2. Fill in the options and criteria"
echo "  3. Record your decision"
echo "  4. Update status when decided"
