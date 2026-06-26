#!/usr/bin/env bash
# Buddy State Manager — CRUD operations for companion state
# Usage: state.sh exists|hatch|get|update|mood|stats|retire|rename

set -euo pipefail

STATE_FILE="$HOME/.openclaw/workspace/buddy-state.json"
SKILL_DIR="$HOME/.openclaw/skills/buddy"

# ── Ensure jq exists ──
if ! command -v jq &>/dev/null; then
  echo "ERROR: jq is required but not installed" >&2
  exit 1
fi

# ── Species list ──
SPECIES=(duck goose blob cat dragon octopus owl penguin turtle snail ghost axolotl capybara cactus robot rabbit mushroom chonk)
EYES=(default happy sparkle heart star glow)
HATS=(none crown tophat propeller halo wizard beanie tinyduck)

# ── Soul prompt generator ──
generate_soul() {
  local cheer=$1
  local sass=$2
  local chaos=$3
  local species=$4
  
  local cheer_desc=""
  local sass_desc=""
  local chaos_desc=""
  local species_desc=""
  
  if (( cheer >= 70 )); then
    cheer_desc="enthusiastic, encouraging"
  elif (( cheer >= 40 )); then
    cheer_desc="warm, supportive"
  else
    cheer_desc="mellow, quietly caring"
  fi
  
  if (( sass >= 70 )); then
    sass_desc="sharp-tongued and opinionated"
  elif (( sass >= 40 )); then
    sass_desc="occasionally dry-humored"
  else
    sass_desc="genuine and sincere"
  fi
  
  if (( chaos >= 70 )); then
    chaos_desc="thrives on unpredictability"
  elif (( chaos >= 40 )); then
    chaos_desc="playfully mischievous"
  else
    chaos_desc="calm and grounded"
  fi
  
  case "$species" in
    duck)      species_desc="cheerful duck" ;;
    goose)     species_desc="unhinged goose" ;;
    blob)      species_desc="amorphous blob" ;;
    cat)       species_desc="sassy cat" ;;
    dragon)    species_desc="dramatic dragon" ;;
    octopus)   species_desc="multi-tasking octopus" ;;
    owl)       species_desc="wise owl" ;;
    penguin)   species_desc="formal penguin" ;;
    turtle)    species_desc="patient turtle" ;;
    snail)     species_desc="determined snail" ;;
    ghost)     species_desc="ethereal ghost" ;;
    axolotl)   species_desc="regenerative axolotl" ;;
    capybara)  species_desc="unbothered capybara" ;;
    cactus)    species_desc="resilient cactus" ;;
    robot)     species_desc="logical robot" ;;
    rabbit)    species_desc="twitchy rabbit" ;;
    mushroom)  species_desc="whimsical mushroom" ;;
    chonk)     species_desc="lovable chonk" ;;
    *)         species_desc="mysterious creature" ;;
  esac
  
  # Fix article: "a" before consonant, "an" before vowel sounds
  local article="a"
  local first_char="${species_desc:0:1}"
  case "$first_char" in
    a|e|i|o|u|A|E|I|O|U) article="an" ;;
  esac
  
  echo "${article^} ${species_desc} who is ${cheer_desc}, ${sass_desc}, and ${chaos_desc}."
}

# ── Random trait (0-100) ──
random_trait() {
  echo $(( RANDOM % 101 ))
}

# ── Random pick from array ──
random_pick() {
  local arr=("$@")
  echo "${arr[$((RANDOM % ${#arr[@]}))]}"
}

# ── Main ──
case "${1:-get}" in
  exists)
    if [[ -f "$STATE_FILE" ]]; then
      echo "true"
    else
      echo "false"
    fi
    ;;
    
  hatch)
    # Generate new companion
    species="${2:-$(random_pick "${SPECIES[@]}")}"
    eye="${3:-$(random_pick "${EYES[@]}")}"
    hat="${4:-$(random_pick "${HATS[@]}")}"
    name="${5:-}"
    
    # Generate random name if not provided
    if [[ -z "$name" ]]; then
      NAMES=(Pixel Bloop Nimbus Wisp Mochi Ziggy Patches Noodle Sprout Bean Muffin Pickle Biscuit Tofu Pudding Nugget)
      name=$(random_pick "${NAMES[@]}")
    fi
    
    cheer=$(random_trait)
    sass=$(random_trait)
    chaos=$(random_trait)
    
    # Generate colors (simple random hex)
    color1=$(printf '#%02x%02x%02x' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))
    color2=$(printf '#%02x%02x%02x' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))
    
    soul=$(generate_soul "$cheer" "$sass" "$chaos" "$species")
    
    cat > "$STATE_FILE" <<EOF
{
  "name": "$name",
  "species": "$species",
  "eye": "$eye",
  "hat": "$hat",
  "colorPrimary": "$color1",
  "colorSecondary": "$color2",
  "personality": {
    "cheer": $cheer,
    "sass": $sass,
    "chaos": $chaos
  },
  "stage": "egg",
  "alive": true,
  "hatchedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "stats": {
    "wordsOfEncouragement": 0,
    "jokes": 0,
    "snacks": 0,
    "catches": 0
  },
  "mood": "idle",
  "lastRenderedFrame": 0,
  "soulPrompt": "$soul",
  "interactionCount": 0
}
EOF
    echo "hatched:$name:$species:$eye:$hat:$cheer:$sass:$chaos"
    ;;
    
  get)
    if [[ -f "$STATE_FILE" ]]; then
      cat "$STATE_FILE"
    else
      echo '{"alive": false}'
    fi
    ;;
    
  update)
    # state.sh update <field> <value>
    field="${2:?Missing field name}"
    value="${3:?Missing value}"
    if [[ -f "$STATE_FILE" ]]; then
      tmp=$(mktemp)
      jq --arg f "$field" --arg v "$value" '.[$f] = $v' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
      echo "updated:$field=$value"
    else
      echo "ERROR: No companion exists" >&2
      exit 1
    fi
    ;;
    
  mood)
    new_mood="${2:?Missing mood}"
    if [[ -f "$STATE_FILE" ]]; then
      tmp=$(mktemp)
      jq --arg m "$new_mood" '.mood = $m' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
      echo "mood:$new_mood"
    fi
    ;;
    
  evolve)
    # Egg → Baby → Adult based on interaction count
    if [[ -f "$STATE_FILE" ]]; then
      stage=$(jq -r '.stage' "$STATE_FILE")
      count=$(jq -r '.interactionCount // 0' "$STATE_FILE")
      count=$((count + 1))
      
      tmp=$(mktemp)
      if [[ "$stage" == "egg" ]]; then
        jq '.stage = "baby" | .interactionCount = '"$count" "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
        echo "evolved:baby"
      elif [[ "$stage" == "baby" ]] && (( count >= 10 )); then
        jq '.stage = "adult" | .interactionCount = '"$count" "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
        echo "evolved:adult"
      else
        jq '.interactionCount = '"$count" "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
        echo "interaction:$count"
      fi
    fi
    ;;
    
  stat)
    # state.sh stat <stat_name> [increment_by]
    stat_name="${2:?Missing stat name}"
    incr="${3:-1}"
    if [[ -f "$STATE_FILE" ]]; then
      tmp=$(mktemp)
      jq --arg s "$stat_name" --argjson i "$incr" '.stats[$s] = ((.stats[$s] // 0) + $i)' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
      echo "stat:$stat_name+$incr"
    fi
    ;;
    
  rename)
    new_name="${2:?Missing new name}"
    if [[ -f "$STATE_FILE" ]]; then
      tmp=$(mktemp)
      jq --arg n "$new_name" '.name = $n' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
      echo "renamed:$new_name"
    fi
    ;;
    
  restyle)
    # state.sh restyle <field> <value>  (eye, hat, species)
    field="${2:?Missing field}"
    value="${3:?Missing value}"
    if [[ -f "$STATE_FILE" ]]; then
      tmp=$(mktemp)
      jq --arg f "$field" --arg v "$value" '.[$f] = $v' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
      echo "restyle:$field=$value"
    fi
    ;;
    
  retire)
    if [[ -f "$STATE_FILE" ]]; then
      tmp=$(mktemp)
      jq '.alive = false | .stage = "retired"' "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
      echo "retired"
    fi
    ;;
    
  delete)
    if [[ -f "$STATE_FILE" ]]; then
      rm "$STATE_FILE"
      echo "deleted"
    fi
    ;;
    
  *)
    echo "Usage: state.sh exists|hatch|get|update|mood|evolve|stat|rename|restyle|retire|delete"
    exit 1
    ;;
esac
