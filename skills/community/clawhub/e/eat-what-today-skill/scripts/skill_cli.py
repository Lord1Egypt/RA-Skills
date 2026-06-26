import argparse
import sys
import io

# Fix Windows console encoding for emoji support
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from eat_what_today import recommend, infer_profile, merge_overrides


def run_recommendation(args):
    query = " ".join(args.query).strip() or "今天吃什么"
    profile = infer_profile(query)
    merge_overrides(profile, args)
    print(recommend(query, args))


def build_parser():
    parser = argparse.ArgumentParser(description="Eat What Today skill CLI")
    parser.add_argument("query", nargs="*", help="用户原始描述")
    parser.add_argument("--weather", choices=["rainy", "cold", "hot", "sunny", "windy", "humid", "all"])
    parser.add_argument("--mood", choices=["happy", "tired", "comfort", "focused", "adventurous", "light", "party", "healthy", "neutral", "sick", "family", "busy"])
    parser.add_argument("--mode", choices=["takeaway", "dine_in", "cook"])
    parser.add_argument("--budget", choices=["low", "mid", "high"])
    parser.add_argument("--spicy", choices=["low", "mid", "high"])
    parser.add_argument("--time_slot", choices=["breakfast", "lunch", "dinner", "late_night"])
    parser.add_argument("--city_tag", choices=["all", "north", "south", "guangdong", "hainan", "hunan"])
    parser.add_argument("--location")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    run_recommendation(args)


if __name__ == "__main__":
    main()
