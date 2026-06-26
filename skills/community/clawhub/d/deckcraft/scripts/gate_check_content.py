#!/usr/bin/env python3
"""
DeckCraft v5 — S3 Content Gate Check
Validates content.json format before rendering.
Catches API format errors that mental review misses.

Usage: python3 gate_check_content.py <content.json_path> <project_dir>
"""
import sys, os, json


def check_content(content_path, project_dir):
    with open(content_path) as f:
        content = json.load(f)

    fail_items = []
    pass_items = []

    pages = content.get("pages", [])

    if len(pages) == 0:
        fail_items.append({
            "check": "has_pages",
            "detail": "content.json has no pages"
        })

    supported_types = {
        "cover", "closing", "toc", "section", "section_divider",
        "content", "content_with_icon",
        "two-col", "vs_compare",
        "table", "stat_cards",
        "chart_bar", "chart_pie", "chart_line", "chart_gauge",
        "timeline", "process_flow", "matrix_2x2",
        "quote", "image_full", "image_split",
        "kpi_dashboard", "team_grid", "checklist",
        "summary", "image"
    }

    for i, page in enumerate(pages):
        idx = page.get("idx", i + 1)

        # 1. Type check
        ptype = page.get("type", "")
        if ptype not in supported_types:
            fail_items.append({
                "check": "valid_type", "slide": idx,
                "detail": f"Unknown type '{ptype}'. Supported: {', '.join(sorted(supported_types))}"
            })
        else:
            pass_items.append({"check": "valid_type", "slide": idx, "detail": f"type={ptype}"})

        # 2. Title check (all pages except cover should have title)
        title = page.get("title", "")
        if not title and ptype != "cover":
            fail_items.append({
                "check": "has_title", "slide": idx,
                "detail": "Missing title"
            })
        elif title:
            if len(title) > 50:
                warnings_item = {"check": "title_length", "slide": idx,
                                 "detail": f"Title '{title[:30]}...' is {len(title)} chars (>50)"}
                # Warning, not failure
                pass_items.append(warnings_item)
            else:
                pass_items.append({"check": "has_title", "slide": idx, "detail": f"OK ({len(title)} chars)"})

        # 3. Key point check (content pages should have key_point)
        key_point = page.get("key_point", "")
        if ptype not in ("cover", "section") and not key_point:
            fail_items.append({
                "check": "has_key_point", "slide": idx,
                "detail": f"Content slide missing key_point (full sentence with insight)"
            })
        elif key_point and len(key_point) < 10:
            fail_items.append({
                "check": "key_point_quality", "slide": idx,
                "detail": f"key_point too short ({len(key_point)} chars): '{key_point}'"
            })

        # 4. Content bullets check
        bullets = page.get("content", [])
        if isinstance(bullets, list) and ptype in ("content", "summary"):
            if len(bullets) > 6:
                fail_items.append({
                    "check": "bullet_count", "slide": idx,
                    "detail": f"{len(bullets)} bullets (max 6)"
                })
            for bi, bullet in enumerate(bullets):
                if isinstance(bullet, str) and len(bullet) > 100:
                    fail_items.append({
                        "check": "bullet_length", "slide": idx,
                        "detail": f"Bullet {bi+1} is {len(bullet)} chars (max 100): '{bullet[:40]}...'"
                    })

        # 5. Table pages need headers and rows
        if ptype == "table":
            headers = page.get("headers", [])
            rows = page.get("rows", [])
            if not headers:
                fail_items.append({
                    "check": "table_headers", "slide": idx,
                    "detail": "Table page missing 'headers'"
                })
            if not rows:
                fail_items.append({
                    "check": "table_rows", "slide": idx,
                    "detail": "Table page missing 'rows'"
                })

        # 6. Two-col pages need left/right content
        if ptype == "two-col":
            if not page.get("left_title") or not page.get("right_title"):
                fail_items.append({
                    "check": "two_col_titles", "slide": idx,
                    "detail": "Two-col page needs left_title and right_title"
                })

        # 7. Image pages should reference an image
        if ptype == "image":
            img = page.get("image", "")
            if not img:
                fail_items.append({
                    "check": "image_source", "slide": idx,
                    "detail": "Image page missing 'image' field"
                })

        # 8. Cover should have title at minimum
        if ptype == "cover" and not title:
            fail_items.append({
                "check": "cover_title", "slide": idx,
                "detail": "Cover page missing title"
            })

    # Global check: cover exists
    cover_exists = any(p.get("type") == "cover" for p in pages)
    if not cover_exists:
        fail_items.append({
            "check": "has_cover",
            "detail": "No cover page found"
        })
    else:
        pass_items.append({"check": "has_cover", "detail": "OK"})

    # Two-col overuse check
    two_col_count = sum(1 for p in pages if p.get("type") == "two-col")
    if two_col_count > 2:
        fail_items.append({
            "check": "two_col_overuse",
            "detail": f"{two_col_count} two-col pages (max 2 recommended)"
        })

    passed = len(fail_items) == 0
    result = {
        "passed": passed,
        "verdict": "PASS — ready for rendering" if passed else "FAIL — fix items before rendering",
        "total_slides": len(pages),
        "fail_count": len(fail_items),
        "pass_count": len(pass_items),
        "fail_items": fail_items,
        "pass_items": pass_items
    }

    os.makedirs(project_dir, exist_ok=True)
    out_path = os.path.join(project_dir, "gate_content.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 gate_check_content.py <content.json_path> <project_dir>")
        print("Output: <project_dir>/gate_content.json")
        sys.exit(1)

    content_path = sys.argv[1]
    project_dir = sys.argv[2]

    if not os.path.exists(content_path):
        result = {
            "passed": False,
            "verdict": "FAIL — content.json not found",
            "fail_items": [{"check": "file_not_found", "detail": content_path}],
            "pass_items": []
        }
        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, "gate_content.json"), "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(json.dumps(result, indent=2))
        sys.exit(1)

    result = check_content(content_path, project_dir)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["passed"]:
        print(f"\n✅ CONTENT GATE PASSED — {result['total_slides']} slides, {result['pass_count']} checks OK")
    else:
        print(f"\n❌ CONTENT GATE FAILED — {result['fail_count']} issue(s):")
        for item in result["fail_items"]:
            slide_info = f"Slide {item['slide']}" if "slide" in item else "Global"
            print(f"   {slide_info}: [{item['check']}] {item['detail']}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
