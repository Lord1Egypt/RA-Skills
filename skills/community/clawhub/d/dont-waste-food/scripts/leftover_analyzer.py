#!/usr/bin/env python3
"""
Dont Waste Food — Leftover Analyzer
Extracts structured ingredient list from natural Indonesian text.
"""
import re
import sys

# Common Indonesian ingredient words with aliases
INGREDIENT_DICT = {
    # Rice & grains
    "nasi": ["nasi", "rice", "nasi sisa", "nasi anget", "nasi hangat"],
    "mie": ["mie", "mi", "noodle", "noodles", "mie telur", "mie instan", "bihun", "sohun", "kwetiau"],
    "roti": ["roti", "bread", "roti tawar", " roti gandum"],
    "lontong": ["lontong"],
    "kentang": ["kentang", "potato"],
    "ubi": ["ubi", "sweet potato", "talas"],

    # Protein
    "telur": ["telur", "egg", "telur ayam", "telur bebek"],
    "ayam": ["ayam", "chicken", "daging ayam", "fillet ayam", "ayam suwir"],
    "ikan": ["ikan", "fish", "fillet ikan"],
    "udang": ["udang", "shrimp", "prawn", "udang windu"],
    "sosis": ["sosis", "sausage"],
    "bakso": ["bakso", "meatball"],
    "daging": ["daging", "meat", "daging sapi", "daging giling"],

    # Tofu & Tempe
    "tahu": ["tahu", "tofu"],
    "tempe": ["tempe", "tempeh"],

    # Vegetables
    "sayuran": ["sayuran", "sayur", "vegetables", "veggies", "sayur hijau"],
    "kangkung": ["kangkung", "water spinach"],
    "bayam": ["bayam", "spinach"],
    "sawi": ["sawi", "mustard green"],
    "kol": ["kol", "cabbage"],
    "tauge": ["tauge", "taoge", "bean sprout"],
    "wortel": ["wortel", "carrot"],
    "jagung": ["jagung", "corn"],
    "labu": ["labu", "pumpkin", "labu kuning"],
    "brokoli": ["brokoli", "broccoli"],
    "jamur": ["jamur", "mushroom"],
    "genjer": ["genjer"],
    "pare": ["pare", "bitter melon"],
    "terong": ["terong", "eggplant", "aubergine"],

    # Herbs & aromatics
    "bawang merah": ["bawang merah", "shallot", "bamer"],
    "bawang putih": ["bawang putih", "garlic", "baput"],
    "bawang": ["bawang", "onion"],
    "cabai": ["cabai", "cabe", "chili", "chilli", "cabai rawit", "cabai merah", "cabai hijau", "lombok"],
    "sambal": ["sambal", "sambal merah", "sambal hijau"],
    "terasi": ["terasi", "shrimp paste", "belacan"],
    "jahe": ["jahe", "ginger"],
    "kunyit": ["kunyit", "turmeric"],
    "kencur": ["kencur", "galangal"],
    "sereh": ["sereh", "lemongrass"],
    "daun salam": ["daun salam", "bay leaf"],
    "daun bawang": ["daun bawang", "spring onion", "scallion"],
    "seledri": ["seledri", "celery"],
    "jeruk nipis": ["jeruk nipis", "lime", "lemon"],
    "tomato": ["tomat", "tomato"],
    "timsun": ["timsun", "cucumber", "mentimun"],

    # Pantry
    "kecap": ["kecap", "kecap manis"],
    "santan": ["santan", "coconut milk", "santan kara"],
    "minyak": ["minyak", "oil", "minyak goreng"],
    "mentega": ["mentega", "butter", "margarin"],
    "garam": ["garam", "salt"],
    "gula": ["gula", "sugar", "gula merah", "gula pasir"],
    "merica": ["merica", "pepper", "lada", "merica bubuk"],
    "penyedap": ["penyedap", "msg", "bumbu penyedap", "royco", "masako"],
    "kaldu": ["kaldu", "stock", "broth", "air kaldu"],
    "tepung": ["tepung", "flour", "tepung terigu", "tepung beras", "tepung tapioka"],
    "kacang": ["kacang", "nuts", "kacang tanah", "kacang hijau", "kacang merah"],

    # Fruits
    "pisang": ["pisang", "banana"],
    "nanas": ["nanas", "pineapple"],
    "alpukat": ["alpukat", "avocado"],
    "jeruk": ["jeruk", "orange"],
    "mangga": ["mangga", "mango"],
    "semangka": ["semangka", "watermelon"],
    "melon": ["melon"],
    "pepaya": ["pepaya", "papaya"],
    "kelapa": ["kelapa", "coconut"],

    # Prepared foods
    "nasi goreng": ["nasi goreng"],
    "sate": ["sate", "satay"],
    "rendang": ["rendang"],
    "opor": ["opor"],
    "gudeg": ["gudeg"],
    "rawon": ["rawon"],
    "soto": ["soto"],
    "gulai": ["gulai"],
    "asinan": ["asinan"],
    "acar": ["acar"],
    "pickle": ["pickle", "acar kuning"],
    "krupuk": ["krupuk", "kerupuk", "rempeyek"],
    "emping": ["emping"],
}


def extract_ingredients(text: str) -> dict:
    """
    Extract ingredients from natural text.
    Returns dict: {'ingredients': [list of found ingredients], 'quantities': {ingredient: qty}}
    """
    text_lower = text.lower()

    found = []
    seen = set()

    # Hierarchical: check longer canonical names first
    sorted_items = sorted(INGREDIENT_DICT.items(), key=lambda x: -len(x[0]))
    matched_ranges = []  # list of (start, end) character positions already matched

    for canonical, aliases in sorted_items:
        if canonical in seen:
            continue
        for alias in aliases:
            pattern = r'\b' + re.escape(alias) + r'\b'
            for m in re.finditer(pattern, text_lower):
                start, end = m.start(), m.end()
                # Check no longer match already covers this position
                already_covered = any(s <= start and end <= e for s, e in matched_ranges)
                if not already_covered:
                    found.append(canonical)
                    seen.add(canonical)
                    matched_ranges.append((start, end))
                    break
            if canonical in seen:
                break

    # Quantities detection
    quantities = {}
    qty_patterns = [
        (r'(\d+)\s*(piring|pelat|mangkok|bungkus|pcs?|piece|potong|potongnya|b',
         r'(bks|batang|butir|siung|lembar|ekor|ons|gram|kg|ml|liter)', text_lower),
    ]

    return {
        "ingredients": found,
        "raw_count": len(found)
    }


def extract_from_text(text: str) -> list:
    """Simple: return list of found ingredient names."""
    result = extract_ingredients(text)
    return result["ingredients"]


def format_ingredient_list(ingredients: list) -> str:
    """Format ingredient list for conversation display."""
    if not ingredients:
        return "Tidak ada bahan yang bisa saya kenali. Coba tulis nama bahannya lebih jelas?"

    unique = list(dict.fromkeys(ingredients))  # preserve order, remove dupes
    return "\n".join([f"  • {i}" for i in unique])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: leftover_analyzer.py '<text>'")
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    ingredients = extract_from_text(text)
    print(f"Ditemukan {len(ingredients)} bahan:")
    print(format_ingredient_list(ingredients))
