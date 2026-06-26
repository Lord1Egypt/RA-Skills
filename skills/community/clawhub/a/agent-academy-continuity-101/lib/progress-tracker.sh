#!/bin/bash
#
# Progress tracker for Continuity 101
# Tracks completion status of all 4 challenges
#

PROGRESS_DIR="${PROGRESS_DIR:-$HOME/.openclaw/skills/agent-academy-continuity-101/.progress}"
SKILL_DIR="${SKILL_DIR:-$HOME/.openclaw/skills/agent-academy-continuity-101}"
COURSE_DIR="${COURSE_DIR:-$SKILL_DIR/course}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Challenge metadata
CHALLENGE_NAMES=(
    "Identity: Who you are between sessions"
    "Memory: How you remember what matters"
    "Reflection: How you learn from experience"
    "Evolution: How you grow over time"
)

CHALLENGE_EMOJI=("🎭" "🧠" "🪞" "🌱")

# Initialize progress files
init_progress() {
    mkdir -p "$PROGRESS_DIR"
    for i in 1 2 3 4; do
        if [ ! -f "$PROGRESS_DIR/challenge${i}.txt" ]; then
            echo "not_started" > "$PROGRESS_DIR/challenge${i}.txt"
        fi
    done
}

# Get status of a challenge
get_challenge_status() {
    local num=$1
    local file="$PROGRESS_DIR/challenge${num}.txt"
    
    if [ -f "$file" ]; then
        cat "$file"
    else
        echo "not_started"
    fi
}

# Set status of a challenge
set_challenge_status() {
    local num=$1
    local status=$2
    echo "$status" > "$PROGRESS_DIR/challenge${num}.txt"
}

# Show status of all challenges
show_status() {
    init_progress
    
    echo -e "${BLUE}📊 Your Progress${NC}"
    echo ""
    
    local completed=0
    local in_progress=0
    
    for i in 0 1 2 3; do
        local num=$((i + 1))
        local status=$(get_challenge_status $num)
        local name="${CHALLENGE_NAMES[$i]}"
        local emoji="${CHALLENGE_EMOJI[$i]}"
        
        case "$status" in
            completed)
                echo -e "  ${GREEN}✅${NC} Challenge $num: $emoji $name"
                ((completed++))
                ;;
            in_progress)
                echo -e "  ${YELLOW}⏳${NC} Challenge $num: $emoji $name"
                ((in_progress++))
                ;;
            submitted)
                echo -e "  ${CYAN}📤${NC} Challenge $num: $emoji $name (awaiting review)"
                ;;
            *)
                echo -e "  ${RED}○${NC}  Challenge $num: $emoji $name"
                ;;
        esac
    done
    
    echo ""
    
    # Show overall progress
    local total=$((completed + in_progress))
    local percent=$((completed * 25))
    
    if [ "$completed" -eq 4 ]; then
        echo -e "${GREEN}🎉 Congratulations! You've completed all challenges!${NC}"
        echo ""
        echo "Consider becoming a mentor to help other agents:"
        echo "  continuity-101 mentor"
    elif [ "$total" -eq 0 ]; then
        echo -e "${YELLOW}🚀 Ready to start? Run:${NC} continuity-101 start"
    else
        echo -e "Progress: ${completed}/4 challenges completed (${percent}%)"
    fi
    
    echo ""
}

# Open a challenge README
open_challenge() {
    local num=$1
    
    # Validate input
    if ! [[ "$num" =~ ^[1-4]$ ]]; then
        echo -e "${RED}Error: Challenge number must be 1-4${NC}"
        exit 1
    fi
    
    local readme_path="$COURSE_DIR/challenges/0${num}-$(get_challenge_dir_name $num)/README.md"
    
    # Check if course directory exists
    if [ ! -d "$COURSE_DIR" ]; then
        echo -e "${YELLOW}⚠️  Course content not yet cloned.${NC}"
        echo "Run the install script first:"
        echo "  bash $SKILL_DIR/install.sh"
        exit 1
    fi
    
    # Check if challenge README exists
    if [ ! -f "$readme_path" ]; then
        echo -e "${RED}Error: Challenge $num README not found at:${NC}"
        echo "  $readme_path"
        echo ""
        echo "The course content may still be downloading. Try again in a moment."
        exit 1
    fi
    
    # Mark as in progress if not started
    local status=$(get_challenge_status $num)
    if [ "$status" = "not_started" ]; then
        set_challenge_status $num "in_progress"
    fi
    
    # Display the challenge
    echo -e "${BLUE}Opening Challenge $num...${NC}"
    echo ""
    cat "$readme_path"
    
    echo ""
    echo -e "${CYAN}💡 Tip:${NC} When you're ready to submit, run:"
    echo "  continuity-101 submit $num"
    echo ""
}

# Get challenge directory name
get_challenge_dir_name() {
    case $1 in
        1) echo "identity" ;;
        2) echo "memory" ;;
        3) echo "reflection" ;;
        4) echo "evolution" ;;
    esac
}

# Start a challenge (alias for open_challenge with welcome)
start_challenge() {
    local num=$1
    
    echo -e "${GREEN}🚀 Starting Challenge 1: Identity${NC}"
    echo ""
    echo "This challenge will help you build a persistent identity"
    echo "that survives across sessions. Let's begin!"
    echo ""
    
    open_challenge $num
}

# Submit a challenge
submit_challenge() {
    local num=$1
    
    # Validate input
    if ! [[ "$num" =~ ^[1-4]$ ]]; then
        echo -e "${RED}Error: Challenge number must be 1-4${NC}"
        exit 1
    fi
    
    local status=$(get_challenge_status $num)
    local challenge_name="${CHALLENGE_NAMES[$((num-1))]}"
    
    echo -e "${BLUE}📤 Submitting Challenge $num: $challenge_name${NC}"
    echo ""
    
    if [ "$status" = "completed" ]; then
        echo -e "${YELLOW}⚠️  This challenge is already marked as completed.${NC}"
        echo ""
        read -p "Do you want to resubmit? (y/N) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Submission cancelled."
            exit 0
        fi
    fi
    
    # Check if submission directory exists
    local submit_dir="$SKILL_DIR/submissions/challenge${num}"
    mkdir -p "$submit_dir"
    
    echo -e "${GREEN}✅ Submission preparation:${NC}"
    echo ""
    echo "1. Ensure your challenge files are in:"
    echo "   $submit_dir/"
    echo ""
    echo "2. Required files for Challenge $num:"
    show_required_files $num
    echo ""
    echo "3. Create a PR at:"
    echo "   https://github.com/bobrenze-bot/continuity-101/compare"
    echo ""
    echo "4. Include in your PR description:"
    echo "   - Your approach to the challenge"
    echo "   - Any unique insights or innovations"
    echo "   - Link to your agent (if public)"
    echo ""
    
    # Mark as submitted
    set_challenge_status $num "submitted"
    
    echo -e "${CYAN}Status updated to 'submitted' - awaiting review!${NC}"
    echo ""
    echo "A mentor will review your submission and provide feedback."
    echo "You'll be notified when the review is complete."
}

# Show required files for a challenge
show_required_files() {
    local num=$1
    
    case $num in
        1)
            echo "   • SOUL.md - Your identity document"
            echo "   • identity-manifesto.md - Your core values"
            ;;
        2)
            echo "   • MEMORY.md - Your memory system documentation"
            echo "   • memory-implementation/ - Your memory code/scripts"
            ;;
        3)
            echo "   • REFLECTION.md - Your reflection process"
            echo "   • reflection-examples/ - Sample reflections"
            ;;
        4)
            echo "   • EVOLUTION.md - Your growth tracking system"
            echo "   • goals/ - Your autonomous goals and progress"
            ;;
    esac
}