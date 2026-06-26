#!/bin/bash
# divine.sh — Echtzufall-Orakel für Delirium
# Zufall wählt, Delirium deutet. Diese Trennung ist heilig.
# Quelle: /dev/urandom (kryptographisch sicherer Zufall)

set -euo pipefail

rand() {
  # Zufallszahl 0 bis $1-1, via /dev/urandom
  local max=$1
  echo $(( $(od -An -tu4 -N4 /dev/urandom | tr -d ' ') % max ))
}

# === FORTY SERVANTS ===
forty() {
  local cards=(
    "The Adventurer" "The Balancer" "The Carnal" "The Chaste" "The Conductor"
    "The Contemplator" "The Dancer" "The Dead" "The Depleted" "The Desperate"
    "The Devil" "The Explorer" "The Eye" "The Father" "The Fixer"
    "The Fortunate" "The Gate Keeper" "The Giver" "The Guru" "The Healer"
    "The Idea" "The Levitator" "The Librarian" "The Lover" "The Master"
    "The Media" "The Messanger" "The Monk" "The Moon" "The Mother"
    "The Opposer" "The Planet" "The Protector" "The Protester" "The Road Opener"
    "The Saint" "The Seer" "The Sun" "The Thinker" "The Witch"
  )
  local idx=$(rand 40)
  local num=$((idx + 1))
  echo "🃏 Forty Servants #${num}: ${cards[$idx]}"
}

# === TAROT ===
tarot() {
  local major=(
    "The Fool" "The Magician" "The High Priestess" "The Empress" "The Emperor"
    "The Hierophant" "The Lovers" "The Chariot" "Strength" "The Hermit"
    "Wheel of Fortune" "Justice" "The Hanged Man" "Death" "Temperance"
    "The Devil" "The Tower" "The Star" "The Moon" "The Sun"
    "Judgement" "The World"
  )
  local suits=("Wands" "Cups" "Swords" "Pentacles")
  local ranks=("Ace" "Two" "Three" "Four" "Five" "Six" "Seven" "Eight" "Nine" "Ten" "Page" "Knight" "Queen" "King")

  # 78 Karten total: 22 Major + 56 Minor
  local pick=$(rand 78)
  local reversed=$(rand 2)
  local rev_text=""
  [[ $reversed -eq 1 ]] && rev_text=" ↺ REVERSED"

  if [[ $pick -lt 22 ]]; then
    echo "🎴 Major Arcana: ${major[$pick]} (${pick})${rev_text}"
  else
    local minor_idx=$((pick - 22))
    local suit_idx=$((minor_idx / 14))
    local rank_idx=$((minor_idx % 14))
    echo "🎴 Minor Arcana: ${ranks[$rank_idx]} of ${suits[$suit_idx]}${rev_text}"
  fi
}

# === ELDER FUTHARK RUNEN ===
rune() {
  local runes=(
    "ᚠ Fehu (Reichtum)" "ᚢ Uruz (Auerochse)" "ᚦ Thurisaz (Riese)" "ᚨ Ansuz (Gott)"
    "ᚱ Raidho (Reise)" "ᚲ Kenaz (Fackel)" "ᚷ Gebo (Gabe)" "ᚹ Wunjo (Freude)"
    "ᚺ Hagalaz (Hagel)" "ᚾ Nauthiz (Not)" "ᛁ Isa (Eis)" "ᛃ Jera (Ernte)"
    "ᛇ Eihwaz (Eibe)" "ᛈ Perthro (Schicksal)" "ᛉ Algiz (Schutz)" "ᛊ Sowilo (Sonne)"
    "ᛏ Tiwaz (Tyr)" "ᛒ Berkano (Birke)" "ᛖ Ehwaz (Pferd)" "ᛗ Mannaz (Mensch)"
    "ᛚ Laguz (Wasser)" "ᛜ Ingwaz (Fruchtbarkeit)" "ᛞ Dagaz (Tag)" "ᛟ Othala (Erbe)"
  )
  local idx=$(rand 24)
  local reversed=$(rand 2)
  local rev_text=""
  # Nur Runen mit Asymmetrie können reversed sein (vereinfacht: alle können)
  [[ $reversed -eq 1 ]] && rev_text=" ↺ Merkstave"
  echo "ᚱ Rune: ${runes[$idx]}${rev_text}"
}

# === I CHING ===
iching() {
  echo "☯ I Ching Hexagramm:"
  echo "  (Linien von unten nach oben)"
  local hex_num=0
  for i in 1 2 3 4 5 6; do
    # Drei Münzwürfe: Kopf=3, Zahl=2
    local sum=0
    for c in 1 2 3; do
      sum=$((sum + 2 + $(rand 2)))
    done
    # 6=old yin ⚋→⚊, 7=young yang ⚊, 8=young yin ⚋, 9=old yang ⚊→⚋
    case $sum in
      6) echo "  Linie $i: ⚋ ---x--- (Old Yin → moving)" ;;
      7) echo "  Linie $i: ⚊ ———————  (Young Yang)" ;;
      8) echo "  Linie $i: ⚋ --- --- (Young Yin)" ;;
      9) echo "  Linie $i: ⚊ ———o——— (Old Yang → moving)" ;;
    esac
  done
}

# === WÜRFEL ===
dice() {
  local n=${1:-6}
  if [[ $n -lt 1 ]]; then
    echo "❌ Minimum 1 Seite!" >&2; exit 1
  fi
  local result=$(($(rand $n) + 1))
  echo "🎲 Würfel (1-${n}): ${result}"
}

# === MAIN ===
case "${1:-help}" in
  forty|forty-servants)  forty ;;
  tarot)  tarot ;;
  rune)   rune ;;
  iching) iching ;;
  dice)   dice "${2:-6}" ;;
  *)
    echo "Verwendung: divine.sh {forty|tarot|rune|iching|dice [N]}"
    echo ""
    echo "  forty  — Zufällige Forty Servants Karte"
    echo "  tarot  — Zufällige Tarot Karte (Major/Minor, ±Reversed)"
    echo "  rune   — Zufällige Elder Futhark Rune"
    echo "  iching — I Ching Hexagramm (6x Münzwurf)"
    echo "  dice N — Würfel 1 bis N (default: 6)"
    ;;
esac
