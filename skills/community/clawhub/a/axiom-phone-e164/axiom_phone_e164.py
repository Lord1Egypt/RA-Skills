"""
🛠️ axiom-phone-e164 — Phone Number E.164 Parser
==================================================

⚠️ LIMITATIONS CONNUES :
- ~30 pays principaux (codes d'indicatif + longueur)
- Pas de numéros spéciaux (111, 911, etc.)
- Pas de validation en temps réel (pas d'appel API)

PARSING ET NORMALISATION E.164
"""

import re
import sys


# Country code → (country name, expected total length with country code)
COUNTRY_DATA = {
    "1": ("US/Canada", 11),  # +1XXXXXXXXXX
    "7": ("Russia/Kazakhstan", 11),
    "20": ("Egypt", 12),
    "27": ("South Africa", 11),
    "30": ("Greece", 12),
    "31": ("Netherlands", 11),
    "32": ("Belgium", 11),
    "33": ("France", 11),
    "34": ("Spain", 11),
    "36": ("Hungary", 11),
    "39": ("Italy", 12),
    "40": ("Romania", 11),
    "41": ("Switzerland", 11),
    "43": ("Austria", 12),
    "44": ("United Kingdom", 12),
    "45": ("Denmark", 10),
    "46": ("Sweden", 11),
    "47": ("Norway", 10),
    "48": ("Poland", 11),
    "49": ("Germany", 12),
    "51": ("Peru", 11),
    "52": ("Mexico", 12),
    "53": ("Cuba", 10),
    "54": ("Argentina", 12),
    "55": ("Brazil", 12),
    "56": ("Chile", 11),
    "57": ("Colombia", 12),
    "58": ("Venezuela", 12),
    "60": ("Malaysia", 11),
    "61": ("Australia", 11),
    "62": ("Indonesia", 12),
    "63": ("Philippines", 12),
    "64": ("New Zealand", 11),
    "65": ("Singapore", 10),
    "66": ("Thailand", 11),
    "81": ("Japan", 11),
    "82": ("South Korea", 12),
    "84": ("Vietnam", 12),
    "86": ("China", 13),
    "90": ("Turkey", 12),
    "91": ("India", 12),
    "92": ("Pakistan", 12),
    "93": ("Afghanistan", 11),
    "94": ("Sri Lanka", 11),
    "95": ("Myanmar", 11),
    "98": ("Iran", 12),
    "211": ("South Sudan", 12),
    "212": ("Morocco", 12),
    "213": ("Algeria", 12),
    "216": ("Tunisia", 11),
    "218": ("Libya", 12),
    "220": ("Gambia", 10),
    "221": ("Senegal", 12),
    "222": ("Mauritania", 11),
    "223": ("Mali", 11),
    "224": ("Guinea", 11),
    "225": ("Ivory Coast", 12),
    "226": ("Burkina Faso", 11),
    "227": ("Niger", 11),
    "228": ("Togo", 10),
    "229": ("Benin", 11),
    "230": ("Mauritius", 10),
    "231": ("Liberia", 10),
    "232": ("Sierra Leone", 10),
    "233": ("Ghana", 11),
    "234": ("Nigeria", 13),
    "235": ("Chad", 11),
    "236": ("Central African Rep.", 11),
    "237": ("Cameroon", 11),
    "238": ("Cape Verde", 10),
    "239": ("São Tomé and Príncipe", 10),
    "240": ("Equatorial Guinea", 11),
    "241": ("Gabon", 10),
    "242": ("Congo", 11),
    "243": ("DR Congo", 11),
    "244": ("Angola", 12),
    "245": ("Guinea-Bissau", 10),
    "246": ("British Indian Ocean", 10),
    "247": ("Ascension", 10),
    "248": ("Seychelles", 10),
    "249": ("Sudan", 12),
    "250": ("Rwanda", 10),
    "251": ("Ethiopia", 12),
    "252": ("Somalia", 10),
    "253": ("Djibouti", 10),
    "254": ("Kenya", 12),
    "255": ("Tanzania", 12),
    "256": ("Uganda", 12),
    "257": ("Burundi", 11),
    "258": ("Mozambique", 12),
    "260": ("Zambia", 12),
    "261": ("Madagascar", 12),
    "262": ("Réunion", 10),
    "263": ("Zimbabwe", 10),
    "264": ("Namibia", 11),
    "265": ("Malawi", 10),
    "266": ("Lesotho", 10),
    "267": ("Botswana", 11),
    "268": ("Eswatini", 10),
    "269": ("Comoros", 10),
    "290": ("Saint Helena", 9),
    "291": ("Eritrea", 10),
    "297": ("Aruba", 10),
    "298": ("Faroe Islands", 9),
    "299": ("Greenland", 9),
    "350": ("Gibraltar", 10),
    "351": ("Portugal", 12),
    "352": ("Luxembourg", 11),
    "353": ("Ireland", 11),
    "354": ("Iceland", 10),
    "355": ("Albania", 11),
    "356": ("Malta", 10),
    "357": ("Cyprus", 10),
    "358": ("Finland", 12),
    "359": ("Bulgaria", 12),
    "370": ("Lithuania", 10),
    "371": ("Latvia", 10),
    "372": ("Estonia", 10),
    "373": ("Moldova", 10),
    "374": ("Armenia", 10),
    "375": ("Belarus", 12),
    "376": ("Andorra", 9),
    "377": ("Monaco", 10),
    "378": ("San Marino", 10),
    "380": ("Ukraine", 11),
    "381": ("Serbia", 12),
    "382": ("Montenegro", 11),
    "383": ("Kosovo", 11),
    "385": ("Croatia", 11),
    "386": ("Slovenia", 10),
    "387": ("Bosnia and Herzegovina", 10),
    "389": ("North Macedonia", 10),
    "420": ("Czech Republic", 12),
    "421": ("Slovakia", 12),
    "423": ("Liechtenstein", 10),
    "500": ("Falkland Islands", 9),
    "501": ("Belize", 9),
    "502": ("Guatemala", 10),
    "503": ("El Salvador", 10),
    "504": ("Honduras", 10),
    "505": ("Nicaragua", 10),
    "506": ("Costa Rica", 10),
    "507": ("Panama", 10),
    "508": ("Saint Pierre and Miquelon", 9),
    "509": ("Haiti", 10),
    "590": ("Guadeloupe", 10),
    "591": ("Bolivia", 11),
    "592": ("Guyana", 9),
    "593": ("Ecuador", 11),
    "594": ("French Guiana", 10),
    "595": ("Paraguay", 11),
    "596": ("Martinique", 10),
    "597": ("Suriname", 10),
    "598": ("Uruguay", 10),
    "670": ("Timor-Leste", 10),
    "672": ("Australian External", 10),
    "673": ("Brunei", 9),
    "674": ("Nauru", 9),
    "675": ("Papua New Guinea", 10),
    "676": ("Tonga", 9),
    "677": ("Solomon Islands", 10),
    "678": ("Vanuatu", 9),
    "679": ("Fiji", 9),
    "680": ("Palau", 10),
    "681": ("Wallis and Futuna", 9),
    "682": ("Cook Islands", 9),
    "683": ("Niue", 9),
    "685": ("Samoa", 9),
    "686": ("Kiribati", 10),
    "687": ("New Caledonia", 9),
    "688": ("Tuvalu", 9),
    "689": ("French Polynesia", 9),
    "690": ("Tokelau", 9),
    "691": ("Micronesia", 10),
    "692": ("Marshall Islands", 10),
    "850": ("North Korea", 11),
    "852": ("Hong Kong", 10),
    "853": ("Macao", 10),
    "855": ("Cambodia", 11),
    "856": ("Laos", 11),
    "880": ("Bangladesh", 12),
    "886": ("Taiwan", 11),
    "960": ("Maldives", 10),
    "961": ("Lebanon", 10),
    "962": ("Jordan", 11),
    "963": ("Syria", 10),
    "964": ("Iraq", 11),
    "965": ("Kuwait", 10),
    "966": ("Saudi Arabia", 11),
    "967": ("Yemen", 11),
    "968": ("Oman", 10),
    "970": ("Palestine", 11),
    "971": ("UAE", 11),
    "972": ("Israel", 11),
    "973": ("Bahrain", 10),
    "974": ("Qatar", 10),
    "975": ("Bhutan", 10),
    "976": ("Mongolia", 10),
    "977": ("Nepal", 11),
    "992": ("Tajikistan", 11),
    "993": ("Turkmenistan", 10),
    "994": ("Azerbaijan", 11),
    "995": ("Georgia", 12),
    "996": ("Kyrgyzstan", 11),
    "998": ("Uzbekistan", 11),
}


def _detect_country_code(digits: str) -> tuple:
    """Detect country code from digit prefix. Returns (code, rest_of_digits)."""
    # Try 3-digit codes first, then 2, then 1
    for length in (3, 2, 1):
        if len(digits) >= length:
            candidate = digits[:length]
            if candidate in COUNTRY_DATA:
                return candidate, digits[length:]
    return None, digits


def parse(phone: str, default_country: str = "33") -> dict:
    """
    Parse and normalize a phone number to E.164 format.

    Args:
        phone: phone number in any format
        default_country: country code to use if not starting with + (default France)

    Returns:
        dict with e164, country_code, country_name, national_number, valid
    """
    if not isinstance(phone, str):
        return {"valid": False, "error": "phone must be a string", "original": str(phone)}

    # Strip non-digit characters except leading +
    has_plus = phone.strip().startswith("+")
    digits = re.sub(r"\D", "", phone)

    if not digits:
        return {"valid": False, "error": "no digits", "original": phone}

    # Determine country code
    if has_plus:
        country_code, national = _detect_country_code(digits)
    else:
        # No +: use default country code
        # Strip leading 0 (trunk prefix) if present
        if digits.startswith("0"):
            digits = digits.lstrip("0") or digits
        country_code = default_country
        national = digits

    if country_code is None:
        return {
            "valid": False,
            "error": f"Unknown country code in: {digits}",
            "original": phone,
        }

    country_name, expected_length = COUNTRY_DATA[country_code]
    e164 = f"+{country_code}{national}"

    # Length check
    if len(e164[1:]) != expected_length:
        return {
            "valid": False,
            "e164": e164,
            "country_code": country_code,
            "country_name": country_name,
            "national_number": national,
            "length": len(e164[1:]),
            "expected_length": expected_length,
            "error": f"Wrong length: {len(e164[1:])} (expected {expected_length})",
            "original": phone,
        }

    return {
        "valid": True,
        "e164": e164,
        "country_code": country_code,
        "country_name": country_name,
        "national_number": national,
        "length": len(e164[1:]),
        "expected_length": expected_length,
        "original": phone,
    }


def is_valid(phone: str) -> bool:
    """Quick check if a phone is valid E.164."""
    try:
        return parse(phone)["valid"]
    except Exception:
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-phone-e164 ")
    parser.add_argument("phone", nargs="?", help="Phone number to parse")
    parser.add_argument("--country", default="33", help="Default country code")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not args.phone:
        # Demo
        examples = [
            "+33 6 12 34 56 78",
            "06 12 34 56 78",
            "(514) 555-1234",
            "+1 555 123 4567",
            "+44 20 7946 0958",
        ]
        for ex in examples:
            result = parse(ex, default_country=args.country)
            icon = "✅" if result["valid"] else "❌"
            print(f"{icon} {ex:<30} → {result.get('e164', '?')}")
        return 0

    result = parse(args.phone, default_country=args.country)
    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        if result["valid"]:
            print(f"✅ E.164: {result['e164']}")
            print(f"   Country: {result['country_name']} (+{result['country_code']})")
        else:
            print(f"❌ {result.get('error', 'invalid')}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
