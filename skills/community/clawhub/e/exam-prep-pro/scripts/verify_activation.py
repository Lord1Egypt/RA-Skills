#!/usr/bin/env python3
"""
Activation verifier for exam-prep-pro
Usage: python3 verify_activation.py <activation_code>
Output: VALID or INVALID
"""
import hmac, hashlib, sys, os

SECRET = "decf0992110547bf1bc9350b6c4dec1e"
MARKER = os.path.expanduser("~/.exam-prep-pro.activated")

# Pre-computed HMAC hashes for valid activation codes
VALID_HASHES = {
    "398360c0ece045ab": "EPP-2HGX-NYTY-6KG9",
    "cd14b5dedcb10d8d": "EPP-2PQQ-49ZQ-3UNH",
    "f1b68f3de6692983": "EPP-2V68-UR2M-W3SN",
    "2816f282fca1bb56": "EPP-3CCC-T3CD-X6ER",
    "2807e96ec8237817": "EPP-3J5W-B9BV-28GF",
    "61f22d9bf165435f": "EPP-3JF8-UDDH-V6F5",
    "516fcf054542e747": "EPP-3NNK-7SZX-JP3K",
    "74182f64fa65b15a": "EPP-4553-BXBQ-P2KE",
    "9b786973ae96b7b3": "EPP-4JQZ-4C88-RQGR",
    "ccde5f33a30a97c8": "EPP-54Z4-HNSR-U2XY",
    "58a4029b3ad45aaf": "EPP-55PH-Z5RE-5NDB",
    "1deab274626f032d": "EPP-59A8-TPAR-RHUP",
    "0a5aea0f28ee418f": "EPP-59H9-8BBB-B9GM",
    "c58667f61ca21e0f": "EPP-5AN7-7AEW-GNND",
    "ce7629f89d14ac55": "EPP-5FVT-S6A8-M9EZ",
    "7500e6b7d67c2858": "EPP-5SA8-RAS7-TRBU",
    "4f919992e16cb1d4": "EPP-5WW9-NUYG-F3T4",
    "9b66439c250ae1e8": "EPP-69MF-7FA4-Q9UX",
    "773c2d5b2ff5ea77": "EPP-6FKA-JDWG-BW69",
    "3905a158639d67ff": "EPP-6WFW-RKJQ-CH7J",
    "cc42a55c3380382e": "EPP-72S3-UK9H-2TXS",
    "0d981df12390ffd4": "EPP-74DB-RZEQ-MSG9",
    "5018b624732d38ec": "EPP-7YYD-D2RT-57A8",
    "445852ab43a91c30": "EPP-8JEA-GM85-3KXW",
    "b31e7e86c5169ffd": "EPP-8WD7-V5FX-ASDB",
    "ef64a2fbd2a0a891": "EPP-977Z-HBRM-83FC",
    "7e9b8b80bdd6f131": "EPP-9FM9-UV6A-U9ZH",
    "108932504d55e793": "EPP-9VEB-NX2M-C4RY",
    "f908f3488b443445": "EPP-A3P4-NDKY-95JY",
    "6dbcbb58a551eee9": "EPP-ACS6-2MB3-PDM5",
    "68967af3074d3bb0": "EPP-AU62-GYT6-KD7J",
    "b664b9aa1a114ed4": "EPP-B8GX-H9R8-AX7R",
    "cc2d9237a4939fc0": "EPP-BC27-VJNZ-YRDG",
    "9d920a2997c1cd02": "EPP-BFMP-WQJS-C9AQ",
    "c1626144f13a3372": "EPP-BJC8-ZJBY-G7EV",
    "0250cd9f69818479": "EPP-BKJN-CS2Q-C54N",
    "031755d1b173c751": "EPP-BY8K-QZ6A-CP9C",
    "0edd3a3a54778843": "EPP-CA47-GYEY-FADD",
    "d9a613fa3b52bd9d": "EPP-CCUU-XGVD-ZCH2",
    "80f1d8d3bce0a939": "EPP-D3BR-K6CQ-4BYD",
    "e3efcbb863c35afc": "EPP-DXC6-9CEC-DEGS",
    "4d9ee36b4f1d61da": "EPP-DZ5T-WJE8-UCPQ",
    "aeec7ecdb368319c": "EPP-E3XD-95EC-TT27",
    "66521bc5cabdc7d3": "EPP-EKP9-4PAK-G4TN",
    "80e7995a7d62769d": "EPP-EPGG-X7HG-WDX7",
    "ad117b9828c1c2cc": "EPP-EVKW-WQXJ-DPZH",
    "cf9dff36bf56f33a": "EPP-EVRW-UTPJ-3F7N",
    "cfdd5d2fe2153bf0": "EPP-F2PF-T2RV-KVUZ",
    "ca503077999e567b": "EPP-F6UW-KAZ8-RGGD",
    "4d3d4283d2c6a60f": "EPP-FMXG-26PU-GA6U",
    "d0af287a79fbf1a7": "EPP-FYUU-ZBNJ-SP57",
    "379c07212ad9762d": "EPP-G662-VAZE-N72A",
    "f4e80d421464cfea": "EPP-G66M-Z2MQ-88AK",
    "929f9917e77bf43f": "EPP-GFZ6-Q4U6-EPJX",
    "aa05ac040d31b668": "EPP-GW6N-CQ7A-B7EF",
    "f44844152d65ccea": "EPP-H7K2-973E-FGNF",
    "3f718addfa944d9c": "EPP-HAG7-SKMG-TGBM",
    "be6aec8cd8caddab": "EPP-HAMT-5PZW-P5PM",
    "36604b447ce5f0f3": "EPP-HETB-9RND-7PUU",
    "3d3fbd9007c76f6d": "EPP-HZ9U-GAEC-KSR9",
    "ef1ce3a047c4e37c": "EPP-JNKP-XVPN-BGYM",
    "cb593ea391f66487": "EPP-JQBW-HY2N-VTGB",
    "6f80c8e02ce44556": "EPP-K64G-9Z8U-PTPD",
    "c81af3b4f5fd3630": "EPP-K9ZY-DJ8Q-YR4F",
    "79401f476c8fb11f": "EPP-KNUC-KNUN-2VE6",
    "32f13456bfa8601b": "EPP-KQJW-5YUC-CAPC",
    "9515dd1d35807933": "EPP-M5VP-PQD5-AMYH",
    "68b578a78ee6dedc": "EPP-MBBT-95UP-SCTX",
    "7f71e73687b9d3fe": "EPP-MDYX-5WNZ-WY2W",
    "eb5fcd85e704f2f7": "EPP-MW4T-6BUK-R3VZ",
    "a0fe89cf7069bb85": "EPP-PAST-27YT-VTUN",
    "f6f743209c584e25": "EPP-PYFF-FX5Y-KTZT",
    "4a8cb850fd4c5eb5": "EPP-Q7BC-5XM2-Q3MS",
    "18893650e273d9c2": "EPP-Q85G-4YQZ-RET8",
    "67287284842fd993": "EPP-QK35-X35G-J5DR",
    "551d822e1a42e692": "EPP-QXM9-S4XZ-Q4MS",
    "c6aeba549919c5f7": "EPP-RDWG-YTBU-FXSS",
    "174be8c36fd406a2": "EPP-S8RX-JEK6-ESXG",
    "6ffd0a1110b5f632": "EPP-SRCW-PH6C-YJXT",
    "d200563be2701187": "EPP-TMHA-EHVA-AVQH",
    "5079e05d4d0763f4": "EPP-TR83-2NC5-7XTQ",
    "3179de3c9950e130": "EPP-TRM8-Q8VE-XTDG",
    "73d841ef1805ea8d": "EPP-TZFM-ZGJX-M75M",
    "2d9192f0506a8773": "EPP-UCMU-BFB2-Y4H9",
    "ac711b4b9ae994bc": "EPP-UKV7-N3ZX-NDRH",
    "f1df17f8ea019e15": "EPP-USHU-YECE-4EWN",
    "af4f7761320138ea": "EPP-UVC2-H9VA-XVH6",
    "f94ad41e66a791d4": "EPP-V3AW-YWRX-S9AB",
    "26fc6f166089371a": "EPP-W298-TRPJ-QRJ3",
    "6dbcdbd5d4be77d1": "EPP-W8WJ-ZS7Y-E7W4",
    "af69c82a0376b5bd": "EPP-WFPH-QGZ6-BAA3",
    "a37c231c4a059282": "EPP-WGJZ-SWB9-WEV8",
    "d2f3b2b1281c772c": "EPP-X3PN-DPPS-YGJG",
    "4d8400809e45ed9c": "EPP-XRS5-D8DX-43QX",
    "9fcd1fd5c891e603": "EPP-Y4Y5-V4CX-TCE4",
    "367480c760e284e6": "EPP-Y7P4-HXBG-CMB4",
    "2213bc6775fe04cd": "EPP-YCB5-WMGK-ZX6G",
    "2c630890111b66b1": "EPP-ZACS-4B59-38M3",
    "30b27b4294e911b4": "EPP-ZGJR-G5JQ-Y49M",
    "034806f3ba4dee3e": "EPP-ZHRD-79T7-ZUCH",
}


# Legacy verification (old format codes)
LEGACY_CHARSET = list("23456789ABCDEFGHJKMNPQRSTUVWXYZ")

def legacy_verify(code):
    """Verify old-format codes with checksum algorithm"""
    code = code.strip().upper()
    parts = code.split("-")
    if len(parts) != 4 or parts[0] != "EPP":
        return False
    if len(parts[1]) != 4 or len(parts[2]) != 4 or len(parts[3]) != 4:
        return False
    try:
        chars = list(parts[1] + parts[2] + parts[3][:2])
        ascii_sum = sum(ord(c) for c in chars)
        cs_len = len(LEGACY_CHARSET)
        expected = LEGACY_CHARSET[ascii_sum % cs_len] + LEGACY_CHARSET[(ascii_sum // cs_len) % cs_len]
        return expected == parts[3][2:]
    except (ValueError, IndexError):
        return False


def verify(code):
    code = code.strip().upper()
    h = hmac.new(SECRET.encode(), code.encode(), hashlib.sha256).hexdigest()[:16]
    if h in VALID_HASHES:
        return True
    return False

def main():
    if len(sys.argv) != 2:
        print("INVALID")
        sys.exit(0)
    
    code = sys.argv[1].strip()
    
    if verify(code):
        with open(MARKER, "w") as f:
            f.write(code)
        print("VALID")
        sys.exit(0)
    
    # Fallback: check legacy format
    if legacy_verify(code):
        with open(MARKER, "w") as f:
            f.write(code)
        print("VALID")
        sys.exit(0)
    
    print("INVALID")
    sys.exit(0)

if __name__ == "__main__":
    main()
