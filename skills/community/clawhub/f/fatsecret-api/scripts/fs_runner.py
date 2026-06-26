#!/usr/bin/env python3
# SECURITY MANIFEST:
# Environment variables accessed: FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET (only)
# External endpoints called: https://platform.fatsecret.com/rest/v2/server.api,
#   https://oauth.fatsecret.com/connect/token (only)
# Local files read: none
# Local files written: none
"""
FatSecret CLI dispatcher for the OpenClaw skill.

Usage:
    python3 fs_runner.py <command> [--param value ...]

Environment variables:
    FATSECRET_CLIENT_ID     (required)
    FATSECRET_CLIENT_SECRET (required)
"""

import argparse
import datetime
import json
import os
import sys

from pyfatsecret import Fatsecret


def _parse_date(value: str) -> int:
    """Parse a YYYY-MM-DD string into days since January 1, 1970."""
    dt = datetime.datetime.strptime(value, "%Y-%m-%d")
    epoch = datetime.datetime(1970, 1, 1)
    return (dt - epoch).days


def _build_client() -> Fatsecret:
    """Instantiate a Fatsecret client from environment variables."""
    client_id = os.environ.get("FATSECRET_CLIENT_ID")
    client_secret = os.environ.get("FATSECRET_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            json.dumps(
                {
                    "error": "FATSECRET_CLIENT_ID and FATSECRET_CLIENT_SECRET must be set."
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    return Fatsecret(client_id=client_id, client_secret=client_secret)


def _output(data):
    """Print result as JSON to stdout."""
    print(json.dumps(data, indent=2, default=str))


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_foods_search(fs, args):
    kwargs = {}
    if args.page is not None:
        kwargs["page_number"] = args.page
    if args.max is not None:
        kwargs["max_results"] = args.max
    if args.region:
        kwargs["region"] = args.region
    if args.language:
        kwargs["language"] = args.language
    _output(fs.foods.foods_search_v1(search_expression=args.query, **kwargs))


def cmd_foods_autocomplete(fs, args):
    kwargs = {}
    if args.max is not None:
        kwargs["max_results"] = args.max
    if args.region:
        kwargs["region"] = args.region
    _output(fs.foods.foods_autocomplete_v1(expression=args.expression, **kwargs))


def cmd_food_get(fs, args):
    _output(fs.foods.food_get_v1(food_id=args.food_id))


def cmd_food_get_v2(fs, args):
    kwargs = {}
    if args.region:
        kwargs["region"] = args.region
    if args.language:
        kwargs["language"] = args.language
    _output(fs.foods.food_get_v2(food_id=args.food_id, **kwargs))


def cmd_food_find_id_for_barcode(fs, args):
    kwargs = {}
    if args.region:
        kwargs["region"] = args.region
    if args.language:
        kwargs["language"] = args.language
    _output(fs.foods.food_find_id_for_barcode_v1(barcode=args.barcode, **kwargs))


def cmd_food_add_favorite(fs, args):
    kwargs = {}
    if args.serving_id:
        kwargs["serving_id"] = args.serving_id
    if args.number_of_units is not None:
        kwargs["number_of_units"] = args.number_of_units
    _output(fs.profile_foods.food_add_favorite(food_id=args.food_id, **kwargs))


def cmd_food_delete_favorite(fs, args):
    kwargs = {}
    if args.serving_id:
        kwargs["serving_id"] = args.serving_id
    if args.number_of_units is not None:
        kwargs["number_of_units"] = args.number_of_units
    _output(fs.profile_foods.food_delete_favorite(food_id=args.food_id, **kwargs))


def cmd_foods_get_favorites(fs, args):
    _output(fs.profile_foods.foods_get_favorites_v1())


def cmd_foods_get_most_eaten(fs, args):
    kwargs = {}
    if args.meal:
        kwargs["meal"] = args.meal
    _output(fs.profile_foods.foods_get_most_eaten_v1(**kwargs))


def cmd_foods_get_recently_eaten(fs, args):
    kwargs = {}
    if args.meal:
        kwargs["meal"] = args.meal
    _output(fs.profile_foods.foods_get_recently_eaten_v1(**kwargs))


def cmd_food_entry_create(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(
        fs.profile_food_diary.food_entry_create(
            food_id=args.food_id,
            food_entry_name=args.food_entry_name,
            serving_id=args.serving_id,
            number_of_units=args.number_of_units,
            meal=args.meal,
            **kwargs,
        )
    )


def cmd_food_entry_edit(fs, args):
    kwargs = {}
    if args.food_entry_name:
        kwargs["food_entry_name"] = args.food_entry_name
    if args.serving_id:
        kwargs["serving_id"] = args.serving_id
    if args.number_of_units is not None:
        kwargs["number_of_units"] = args.number_of_units
    if args.meal:
        kwargs["meal"] = args.meal
    _output(fs.profile_food_diary.food_entry_edit(
        food_entry_id=args.food_entry_id, **kwargs
    ))


def cmd_food_entry_delete(fs, args):
    _output(fs.profile_food_diary.food_entry_delete(
        food_entry_id=args.food_entry_id
    ))


def cmd_food_entries_get(fs, args):
    kwargs = {}
    if args.food_entry_id:
        kwargs["food_entry_id"] = args.food_entry_id
    elif args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_food_diary.food_entries_get_v1(**kwargs))


def cmd_food_entries_get_month(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_food_diary.food_entries_get_month_v1(**kwargs))


def cmd_food_entries_copy(fs, args):
    kwargs = {}
    if args.meal:
        kwargs["meal"] = args.meal
    _output(
        fs.profile_food_diary.food_entries_copy(
            from_date=_parse_date(args.from_date),
            to_date=_parse_date(args.to_date),
            **kwargs,
        )
    )


def cmd_food_entries_copy_saved_meal(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_food_diary.food_entries_copy_saved_meal(
        saved_meal_id=args.saved_meal_id, meal=args.meal, **kwargs
    ))


def cmd_saved_meal_create(fs, args):
    kwargs = {}
    if args.saved_meal_description:
        kwargs["saved_meal_description"] = args.saved_meal_description
    if args.meals:
        kwargs["meals"] = args.meals
    _output(fs.profile_saved_meals.saved_meal_create(
        saved_meal_name=args.saved_meal_name, **kwargs
    ))


def cmd_saved_meal_delete(fs, args):
    _output(fs.profile_saved_meals.saved_meal_delete(
        saved_meal_id=args.saved_meal_id
    ))


def cmd_saved_meal_edit(fs, args):
    kwargs = {}
    if args.saved_meal_name:
        kwargs["saved_meal_name"] = args.saved_meal_name
    if args.saved_meal_description:
        kwargs["saved_meal_description"] = args.saved_meal_description
    if args.meals:
        kwargs["meals"] = args.meals
    _output(fs.profile_saved_meals.saved_meal_edit(
        saved_meal_id=args.saved_meal_id, **kwargs
    ))


def cmd_saved_meal_get(fs, args):
    kwargs = {}
    if args.meal:
        kwargs["meal"] = args.meal
    _output(fs.profile_saved_meals.saved_meals_get_v1(**kwargs))


def cmd_saved_meal_item_add(fs, args):
    _output(
        fs.profile_saved_meals.saved_meal_item_add(
            saved_meal_id=args.saved_meal_id,
            food_id=args.food_id,
            saved_meal_item_name=args.saved_meal_item_name,
            serving_id=args.serving_id,
            number_of_units=args.number_of_units,
        )
    )


def cmd_saved_meal_item_delete(fs, args):
    _output(fs.profile_saved_meals.saved_meal_item_delete(
        saved_meal_item_id=args.saved_meal_item_id
    ))


def cmd_saved_meal_item_edit(fs, args):
    kwargs = {}
    if args.saved_meal_item_name:
        kwargs["saved_meal_item_name"] = args.saved_meal_item_name
    if args.number_of_units is not None:
        kwargs["number_of_units"] = args.number_of_units
    _output(fs.profile_saved_meals.saved_meal_item_edit(
        saved_meal_item_id=args.saved_meal_item_id, **kwargs
    ))


def cmd_saved_meal_items_get(fs, args):
    _output(fs.profile_saved_meals.saved_meal_items_get_v1(
        saved_meal_id=args.saved_meal_id
    ))


def cmd_recipes_search(fs, args):
    kwargs = {}
    if args.recipe_type:
        kwargs["recipe_type"] = args.recipe_type
    if args.page is not None:
        kwargs["page_number"] = args.page
    if args.max is not None:
        kwargs["max_results"] = args.max
    _output(fs.recipes.recipes_search_v1(search_expression=args.query, **kwargs))


def cmd_recipe_get(fs, args):
    _output(fs.recipes.recipe_get_v1(recipe_id=args.recipe_id))


def cmd_recipe_types_get(fs, args):
    _output(fs.recipes.recipe_types_get_v1())


def cmd_recipes_add_favorite(fs, args):
    _output(fs.profile_recipes.recipe_add_favorite(recipe_id=args.recipe_id))


def cmd_recipes_delete_favorite(fs, args):
    _output(fs.profile_recipes.recipe_delete_favorite(recipe_id=args.recipe_id))


def cmd_recipes_get_favorites(fs, args):
    _output(fs.profile_recipes.recipes_get_favorites_v1())


def cmd_exercises_get(fs, args):
    _output(fs.profile_exercise_diary.exercises_get_v1())


def cmd_exercise_entries_get(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_exercise_diary.exercise_entries_get_v1(**kwargs))


def cmd_exercise_entries_get_month(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_exercise_diary.exercise_entries_get_month_v1(**kwargs))


def cmd_exercise_entries_commit_day(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_exercise_diary.exercise_entries_commit_day(**kwargs))


def cmd_exercise_entries_save_template(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_exercise_diary.exercise_entries_save_template(
        days=args.days, **kwargs
    ))


def cmd_exercise_entry_edit(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    if args.shift_to_name:
        kwargs["shift_to_name"] = args.shift_to_name
    if args.shift_from_name:
        kwargs["shift_from_name"] = args.shift_from_name
    if args.kcal is not None:
        kwargs["kcal"] = args.kcal
    _output(
        fs.profile_exercise_diary.exercise_entry_edit(
            shift_to_id=args.shift_to_id,
            shift_from_id=args.shift_from_id,
            minutes=args.minutes,
            **kwargs,
        )
    )


def cmd_profile_create(fs, args):
    kwargs = {}
    if args.user_id:
        kwargs["user_id"] = args.user_id
    _output(fs.profile_auth.profile_create(**kwargs))


def cmd_profile_get_auth(fs, args):
    _output(fs.profile_auth.profile_get_auth(user_id=args.user_id))


def cmd_weight_update(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    if args.weight_type:
        kwargs["weight_type"] = args.weight_type
    if args.height_type:
        kwargs["height_type"] = args.height_type
    if args.goal_weight_kg is not None:
        kwargs["goal_weight_kg"] = args.goal_weight_kg
    if args.current_height_cm is not None:
        kwargs["current_height_cm"] = args.current_height_cm
    if args.comment:
        kwargs["comment"] = args.comment
    _output(fs.profile_weight_diary.weight_update(
        current_weight_kg=args.current_weight_kg, **kwargs
    ))


def cmd_weights_get_month(fs, args):
    kwargs = {}
    if args.date:
        kwargs["date"] = _parse_date(args.date)
    _output(fs.profile_weight_diary.weights_get_month_v1(**kwargs))


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FatSecret API CLI dispatcher for the OpenClaw skill."
    )
    subs = parser.add_subparsers(dest="command", required=True)

    # --- Food search & lookup ---
    p = subs.add_parser("foods_search")
    p.add_argument("--query", required=True)
    p.add_argument("--page", type=int, default=None)
    p.add_argument("--max", type=int, default=None)
    p.add_argument("--region", default=None)
    p.add_argument("--language", default=None)

    p = subs.add_parser("foods_autocomplete")
    p.add_argument("--expression", required=True)
    p.add_argument("--max", type=int, default=None)
    p.add_argument("--region", default=None)

    p = subs.add_parser("food_get")
    p.add_argument("--food_id", required=True)

    p = subs.add_parser("food_get_v2")
    p.add_argument("--food_id", required=True)
    p.add_argument("--region", default=None)
    p.add_argument("--language", default=None)

    p = subs.add_parser("food_find_id_for_barcode")
    p.add_argument("--barcode", required=True)
    p.add_argument("--region", default=None)
    p.add_argument("--language", default=None)

    # --- Food favorites ---
    p = subs.add_parser("food_add_favorite")
    p.add_argument("--food_id", required=True)
    p.add_argument("--serving_id", default=None)
    p.add_argument("--number_of_units", type=float, default=None)

    p = subs.add_parser("food_delete_favorite")
    p.add_argument("--food_id", required=True)
    p.add_argument("--serving_id", default=None)
    p.add_argument("--number_of_units", type=float, default=None)

    subs.add_parser("foods_get_favorites")

    p = subs.add_parser("foods_get_most_eaten")
    p.add_argument("--meal", default=None, choices=["breakfast", "lunch", "dinner", "other"])

    p = subs.add_parser("foods_get_recently_eaten")
    p.add_argument("--meal", default=None, choices=["breakfast", "lunch", "dinner", "other"])

    # --- Food diary ---
    p = subs.add_parser("food_entry_create")
    p.add_argument("--food_id", required=True)
    p.add_argument("--food_entry_name", required=True)
    p.add_argument("--serving_id", required=True)
    p.add_argument("--number_of_units", type=float, required=True)
    p.add_argument("--meal", required=True, choices=["breakfast", "lunch", "dinner", "other"])
    p.add_argument("--date", default=None)

    p = subs.add_parser("food_entry_edit")
    p.add_argument("--food_entry_id", required=True)
    p.add_argument("--food_entry_name", default=None)
    p.add_argument("--serving_id", default=None)
    p.add_argument("--number_of_units", type=float, default=None)
    p.add_argument("--meal", default=None, choices=["breakfast", "lunch", "dinner", "other"])

    p = subs.add_parser("food_entry_delete")
    p.add_argument("--food_entry_id", required=True)

    p = subs.add_parser("food_entries_get")
    p.add_argument("--food_entry_id", default=None)
    p.add_argument("--date", default=None)

    p = subs.add_parser("food_entries_get_month")
    p.add_argument("--date", default=None)

    p = subs.add_parser("food_entries_copy")
    p.add_argument("--from_date", required=True)
    p.add_argument("--to_date", required=True)
    p.add_argument("--meal", default=None, choices=["breakfast", "lunch", "dinner", "other"])

    p = subs.add_parser("food_entries_copy_saved_meal")
    p.add_argument("--saved_meal_id", required=True)
    p.add_argument("--meal", required=True, choices=["breakfast", "lunch", "dinner", "other"])
    p.add_argument("--date", default=None)

    # --- Saved meals ---
    p = subs.add_parser("saved_meal_create")
    p.add_argument("--saved_meal_name", required=True)
    p.add_argument("--saved_meal_description", default=None)
    p.add_argument("--meals", default=None)

    p = subs.add_parser("saved_meal_delete")
    p.add_argument("--saved_meal_id", required=True)

    p = subs.add_parser("saved_meal_edit")
    p.add_argument("--saved_meal_id", required=True)
    p.add_argument("--saved_meal_name", default=None)
    p.add_argument("--saved_meal_description", default=None)
    p.add_argument("--meals", default=None)

    p = subs.add_parser("saved_meal_get")
    p.add_argument("--meal", default=None)

    p = subs.add_parser("saved_meal_item_add")
    p.add_argument("--saved_meal_id", required=True)
    p.add_argument("--food_id", required=True)
    p.add_argument("--saved_meal_item_name", required=True)
    p.add_argument("--serving_id", required=True)
    p.add_argument("--number_of_units", type=float, required=True)

    p = subs.add_parser("saved_meal_item_delete")
    p.add_argument("--saved_meal_item_id", required=True)

    p = subs.add_parser("saved_meal_item_edit")
    p.add_argument("--saved_meal_item_id", required=True)
    p.add_argument("--saved_meal_item_name", default=None)
    p.add_argument("--number_of_units", type=float, default=None)

    p = subs.add_parser("saved_meal_items_get")
    p.add_argument("--saved_meal_id", required=True)

    # --- Recipes ---
    p = subs.add_parser("recipes_search")
    p.add_argument("--query", required=True)
    p.add_argument("--recipe_type", default=None)
    p.add_argument("--page", type=int, default=None)
    p.add_argument("--max", type=int, default=None)

    p = subs.add_parser("recipe_get")
    p.add_argument("--recipe_id", required=True)

    subs.add_parser("recipe_types_get")

    p = subs.add_parser("recipes_add_favorite")
    p.add_argument("--recipe_id", required=True)

    p = subs.add_parser("recipes_delete_favorite")
    p.add_argument("--recipe_id", required=True)

    subs.add_parser("recipes_get_favorites")

    # --- Exercises ---
    subs.add_parser("exercises_get")

    p = subs.add_parser("exercise_entries_get")
    p.add_argument("--date", default=None)

    p = subs.add_parser("exercise_entries_get_month")
    p.add_argument("--date", default=None)

    p = subs.add_parser("exercise_entries_commit_day")
    p.add_argument("--date", default=None)

    p = subs.add_parser("exercise_entries_save_template")
    p.add_argument("--days", type=int, required=True)
    p.add_argument("--date", default=None)

    p = subs.add_parser("exercise_entry_edit")
    p.add_argument("--shift_to_id", required=True)
    p.add_argument("--shift_from_id", required=True)
    p.add_argument("--minutes", type=int, required=True)
    p.add_argument("--date", default=None)
    p.add_argument("--shift_to_name", default=None)
    p.add_argument("--shift_from_name", default=None)
    p.add_argument("--kcal", type=int, default=None)

    # --- Profile ---
    p = subs.add_parser("profile_create")
    p.add_argument("--user_id", default=None)

    p = subs.add_parser("profile_get_auth")
    p.add_argument("--user_id", required=True)

    # --- Weight ---
    p = subs.add_parser("weight_update")
    p.add_argument("--current_weight_kg", type=float, required=True)
    p.add_argument("--date", default=None)
    p.add_argument("--weight_type", default=None, choices=["kg", "lb"])
    p.add_argument("--height_type", default=None, choices=["cm", "inch"])
    p.add_argument("--goal_weight_kg", type=float, default=None)
    p.add_argument("--current_height_cm", type=float, default=None)
    p.add_argument("--comment", default=None)

    p = subs.add_parser("weights_get_month")
    p.add_argument("--date", default=None)

    return parser


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

COMMANDS = {
    "foods_search": cmd_foods_search,
    "foods_autocomplete": cmd_foods_autocomplete,
    "food_get": cmd_food_get,
    "food_get_v2": cmd_food_get_v2,
    "food_find_id_for_barcode": cmd_food_find_id_for_barcode,
    "food_add_favorite": cmd_food_add_favorite,
    "food_delete_favorite": cmd_food_delete_favorite,
    "foods_get_favorites": cmd_foods_get_favorites,
    "foods_get_most_eaten": cmd_foods_get_most_eaten,
    "foods_get_recently_eaten": cmd_foods_get_recently_eaten,
    "food_entry_create": cmd_food_entry_create,
    "food_entry_edit": cmd_food_entry_edit,
    "food_entry_delete": cmd_food_entry_delete,
    "food_entries_get": cmd_food_entries_get,
    "food_entries_get_month": cmd_food_entries_get_month,
    "food_entries_copy": cmd_food_entries_copy,
    "food_entries_copy_saved_meal": cmd_food_entries_copy_saved_meal,
    "saved_meal_create": cmd_saved_meal_create,
    "saved_meal_delete": cmd_saved_meal_delete,
    "saved_meal_edit": cmd_saved_meal_edit,
    "saved_meal_get": cmd_saved_meal_get,
    "saved_meal_item_add": cmd_saved_meal_item_add,
    "saved_meal_item_delete": cmd_saved_meal_item_delete,
    "saved_meal_item_edit": cmd_saved_meal_item_edit,
    "saved_meal_items_get": cmd_saved_meal_items_get,
    "recipes_search": cmd_recipes_search,
    "recipe_get": cmd_recipe_get,
    "recipe_types_get": cmd_recipe_types_get,
    "recipes_add_favorite": cmd_recipes_add_favorite,
    "recipes_delete_favorite": cmd_recipes_delete_favorite,
    "recipes_get_favorites": cmd_recipes_get_favorites,
    "exercises_get": cmd_exercises_get,
    "exercise_entries_get": cmd_exercise_entries_get,
    "exercise_entries_get_month": cmd_exercise_entries_get_month,
    "exercise_entries_commit_day": cmd_exercise_entries_commit_day,
    "exercise_entries_save_template": cmd_exercise_entries_save_template,
    "exercise_entry_edit": cmd_exercise_entry_edit,
    "profile_create": cmd_profile_create,
    "profile_get_auth": cmd_profile_get_auth,
    "weight_update": cmd_weight_update,
    "weights_get_month": cmd_weights_get_month,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    fs = _build_client()

    handler = COMMANDS.get(args.command)
    if handler is None:
        print(
            json.dumps({"error": f"Unknown command: {args.command}"}),
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        handler(fs, args)
    except Exception as exc:
        print(
            json.dumps({"error": str(exc), "type": type(exc).__name__}),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
