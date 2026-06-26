#!/bin/bash
# intuition.sh — Random interpretation impulses for divination readings
# Poetic, evocative, never generic. Powered by /dev/urandom.
# Part of the Divination Skill — "At every crossroads lies a message."
set -euo pipefail

IMPULSE=(
  # Elements & Matter
  "fire" "water" "earth" "air" "ether"
  "salt" "mercury" "sulfur" "ash" "obsidian"
  "amber" "iron" "copper" "silver" "gold"
  "glass" "tar" "wax" "dust" "smoke"
  "quartz" "clay" "charcoal" "pearl" "coral"
  "bronze" "lead" "jade" "onyx" "lava"
  "ice" "resin" "pitch" "thorn" "seed"
  # Body
  "left hand" "right hand" "spine" "throat" "third eye"
  "tongue" "navel" "heartbeat" "bone" "blood"
  "breath" "skin" "scar" "tendon" "pupil"
  "vein" "skull" "palm" "tooth" "marrow"
  "sinew" "membrane" "iris" "tear" "bile"
  # Times & Sky
  "twilight" "midnight" "dawn" "zenith" "blue hour"
  "moonrise" "solar eclipse" "polar night" "witching hour" "gloaming"
  "sunset" "nadir" "blood moon" "starfall" "eventide"
  "vesper" "cockcrow" "nebula" "crescent" "void"
  # Weather & Nature
  "thunderstorm" "fog" "frost" "storm surge" "stillness"
  "hail" "dew" "heat shimmer" "aurora" "stagnant air"
  "landslide" "spring tide" "foehn" "hoarfrost" "sandstorm"
  "blizzard" "drought" "deluge" "whirlwind" "tempest"
  "lightning" "mirage" "avalanche" "erosion" "mycelium"
  # Animals
  "raven" "snake" "spider" "wolf" "eel"
  "falcon" "moth" "octopus" "toad" "dragonfly"
  "hyena" "crow" "worm" "coyote" "seahorse"
  "panther" "fox" "owl" "stag" "hare"
  "serpent" "phoenix" "whale" "scorpion" "beetle"
  "vulture" "lynx" "bat" "jellyfish" "swan"
  # Emotions & States
  "pride" "shame" "longing" "defiance" "ecstasy"
  "melancholy" "wrath" "wonder" "emptiness" "greed"
  "confusion" "clarity" "disgust" "euphoria" "resignation"
  "impatience" "humility" "paranoia" "sanctuary" "madness"
  "sorrow" "courage" "dread" "nostalgia" "rapture"
  "solitude" "belonging" "bitterness" "vulnerability" "awakening"
  # Abstract Concepts
  "threshold" "mirror" "labyrinth" "key" "mask"
  "echo" "shadow" "knot" "abyss" "horizon"
  "boundary" "spiral" "crack" "silence" "resonance"
  "bridge" "root" "fragment" "reversal" "compression"
  "veil" "portal" "cycle" "vortex" "rift"
  "ember" "spark" "memory" "dream" "current"
  # Colors
  "blood red" "midnight blue" "bone white" "emerald" "violet"
  "ochre" "pitch black" "rust" "moon silver" "venom green"
  "crimson" "indigo" "scarlet" "azure" "vermillion"
  "charcoal" "ivory" "turquoise" "lapis" "amethyst"
  # Places & Spaces
  "crossroad" "well" "ruin" "cemetery" "cave"
  "tower" "harbor" "cellar" "clearing" "temple"
  "shrine" "altar" "grove" "desert" "shore"
  "cliff" "marsh" "catacomb" "sanctum" "wasteland"
  "underworld" "otherworld" "limbo" "wildwood" "frontier"
  # Actions
  "burn" "bury" "break" "open" "seal"
  "whisper" "scream" "wait" "fall" "dissolve"
  "rise" "flow" "freeze" "melt" "weave"
  "unravel" "sever" "bind" "reveal" "conceal"
  "transform" "awaken" "remember" "forget" "forgive"
  "choose" "renounce" "embrace" "release" "summon"
  "sacrifice" "consecrate" "bless" "curse" "invoke"
  # Crossroads & Liminal
  "crossroads" "threshold" "messenger" "trickster" "offering"
  "gate" "choice" "path" "junction" "between"
  "neither" "both" "coin" "riddle" "bargain"
  "pact" "wanderer" "stranger" "guide" "omen"
  "toll" "passage" "fork" "road" "pilgrim"
  "shape-shifter" "shadow self" "double" "oracle" "fool"
  "stepping stone" "beacon" "signpost" "compass" "origin"
  "still point" "zero" "infinite" "eternal" "moment"
)

rand() {
  echo $(( $(od -An -tu4 -N4 /dev/urandom | tr -d ' ') % $1 ))
}

count=${1:-3}
[[ $count -gt 5 ]] && count=5
[[ $count -lt 1 ]] && count=1

total=${#IMPULSE[@]}
result=()
used=()

for ((i=0; i<count; i++)); do
  while true; do
    idx=$(rand $total)
    dup=0
    for u in "${used[@]+"${used[@]}"}"; do
      [[ "$u" == "$idx" ]] && dup=1 && break
    done
    [[ $dup -eq 0 ]] && break
  done
  used+=("$idx")
  result+=("${IMPULSE[$idx]}")
done

out=""
for r in "${result[@]}"; do
  [[ -n "$out" ]] && out="$out · "
  out="$out$r"
done
echo "✦ $out"
