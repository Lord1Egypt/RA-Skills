#!/usr/bin/env python3
"""
Dont Waste Food — Recipe Matcher
Matches user ingredient input to Indonesian recipes.
Pantry staples are excluded from scoring penalty.
"""
import json
import os
import sys

RECIPE_FILE = os.path.join(os.path.dirname(__file__), "../references/resep_indonesia.json")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../../workspace/dont-waste-food")


def load_recipes():
    with open(RECIPE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["recipes"], data.get("pantry_staples", [])


def normalize(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str) -> list:
    """Split input into ingredient words/phrases."""
    text = text.replace(",", " ").replace(" dan ", " ").replace(" sama ", " ").replace(" dengan ", " ")
    return [t.strip().lower() for t in text.split() if len(t.strip()) > 1]


def is_pantry(ingredient: str, pantry: list) -> bool:
    ing_n = normalize(ingredient)
    for p in pantry:
        if ing_n in normalize(p) or normalize(p) in ing_n:
            return True
    return False


def ingredient_match(user_input: str, recipe_ingredients: list, pantry: list) -> tuple:
    """
    Returns (match_score_0_100, matched, missing).
    Pantry staples excluded from scoring.
    """
    tokens = tokenize(user_input)
    tokens_n = {normalize(t) for t in tokens}

    matched = []
    scored_missing = []

    for ing in recipe_ingredients:
        ing_n = normalize(ing)
        ing_is_pantry = is_pantry(ing, pantry)

        # Check if ingredient is mentioned
        found = any(
            t in ing_n or ing_n in t or
            t.replace(" ", "") in ing_n or ing_n.replace(" ", "") in t
            for t in tokens_n
        )

        if found:
            matched.append(ing)
        elif not ing_is_pantry:
            scored_missing.append(ing)

    scored_ingredients = [i for i in recipe_ingredients if not is_pantry(i, pantry)]
    if scored_ingredients:
        score = int((len([m for m in scored_ingredients if m in matched]) / len(scored_ingredients)) * 100)
    else:
        score = 100

    return score, matched, scored_missing


def find_recipes(user_input: str, threshold: int = 30, top_n: int = 3) -> list:
    """Find top matching recipes. Returns list of dicts with recipe + match info."""
    recipes, pantry = load_recipes()
    results = []

    for recipe in recipes:
        score, matched, missing = ingredient_match(user_input, recipe["ingredients"], pantry)
        opt_matched = [o for o in recipe.get("optional_ingredients", [])
                       if any(normalize(o) in normalize(user_input) for _ in [1])]

        results.append({
            "recipe": recipe,
            "match_score": score,
            "matched": matched,
            "missing": missing,
            "optional_matched": opt_matched
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    passing = [r for r in results if r["match_score"] >= threshold]
    if not passing:
        passing = results[:2]  # fallback: show best available

    return passing[:top_n]


def format_recipe_suggestion(result: dict, index: int = 1) -> str:
    """Format a recipe suggestion for display in conversation."""
    recipe = result["recipe"]
    score = result["match_score"]
    matched = result["matched"]
    missing = result["missing"]
    opt_matched = result["optional_matched"]

    emoji = "🔥" if score >= 80 else "✨" if score >= 60 else "👌"

    lines = [
        f"{emoji} *{index}. {recipe['name']}*",
        f"   Match: *{score}%* | ⏱️ {recipe['time_min']} menit | 📊 {recipe['difficulty']}",
        f"   {recipe['description']}",
    ]

    if matched:
        lines.append(f"   ✅ *Sudah ada:* {', '.join(matched)}")
    if missing:
        lines.append(f"   ➕ *Butuh tambahan:* {', '.join(missing)}")
    if opt_matched:
        lines.append(f"   🎯 *Bonus:* {', '.join(opt_matched)}")

    return "\n".join(lines)


def format_recipe_full(recipe: dict) -> str:
    """Format full recipe for display in cooking guide."""
    lines = [
        f"🍳 *{recipe['name']}*",
        f"⏱️ Waktu: {recipe['time_min']} menit | 📊 Tingkat: {recipe['difficulty']}",
        f"",
        f"_{recipe['description']}_",
        f"",
    ]

    all_ing = recipe["ingredients"] + recipe.get("optional_ingredients", [])
    lines.append(f"📋 *Bahan:*")
    for i in all_ing:
        lines.append(f"  • {i}")
    lines.append("")

    if recipe.get("safety_notes"):
        lines.append("⚠️ *Catatan Keamanan:*")
        for note in recipe["safety_notes"]:
            lines.append(f"  • {note}")
        lines.append("")

    return "\n".join(lines)


def get_step(recipe: dict, step_number: int) -> str:
    """Get a specific step."""
    steps = recipe["steps"]
    if 1 <= step_number <= len(steps):
        return steps[step_number - 1]
    return None


def get_recipe_by_id(recipe_id: str) -> dict:
    recipes, _ = load_recipes()
    for r in recipes:
        if r["id"] == recipe_id:
            return r
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: recipe_matcher.py '<ingredient text>'")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    results = find_recipes(user_input)

    if not results:
        print("Tidak ada resep cocok ditemukan.")
    else:
        for i, r in enumerate(results, 1):
            print(format_recipe_suggestion(r, i))
            print()
