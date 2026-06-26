#!/usr/bin/env python3
"""
App UI Explorer - Crawl an Android app via ADB accessibility tree.

Classifies clickable elements into:
  - NAVIGATE: opens a new Activity → explore recursively, then BACK
  - TAB:      same Activity, content changes → screenshot in place, no BACK
  - INPUT:    text field / keyboard trigger → skip
  - NOOP:     nothing changed → skip

Usage:
    python3 app_explorer.py <package_name> [--depth 3] [--output ./explore_output]
"""

import subprocess
import xml.etree.ElementTree as ET
import hashlib
import json
import os
import re
import time
import argparse
from dataclasses import dataclass, field
from typing import Optional


# Classes that are typically text input fields
INPUT_CLASSES = {
    "android.widget.EditText",
    "android.widget.AutoCompleteTextView",
    "android.widget.MultiAutoCompleteTextView",
    "android.widget.SearchView",
}

# Resource-id patterns that suggest input fields
INPUT_ID_PATTERNS = ["search", "edit", "input", "query", "text_field"]


@dataclass
class ClickableElement:
    index: int
    label: str
    class_name: str
    resource_id: str
    center: tuple
    bounds: tuple
    element_type: str = "unknown"  # navigate, tab, input, unknown


@dataclass
class PageNode:
    page_id: str
    activity: str
    title: str
    screenshot: str
    clickables: list = field(default_factory=list)
    children: list = field(default_factory=list)
    tabs: list = field(default_factory=list)  # tab content snapshots


class AppExplorer:
    def __init__(self, package: str, output_dir: str, max_depth: int = 3,
                 wait_after_tap: float = 2.0, wait_after_back: float = 1.0):
        self.package = package
        self.output_dir = output_dir
        self.max_depth = max_depth
        self.wait_after_tap = wait_after_tap
        self.wait_after_back = wait_after_back
        self.visited_pages: set = set()  # activity-level dedup
        self.visited_tabs: set = set()   # tab content dedup
        self.screenshot_count = 0
        self.dump_file = os.path.join(output_dir, "_ui_dump.xml")

        os.makedirs(output_dir, exist_ok=True)

    # --- ADB helpers ---

    def adb(self, *args, timeout=15) -> str:
        try:
            result = subprocess.run(
                ["adb", "shell"] + list(args),
                capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return ""

    def adb_host(self, *args, timeout=15) -> str:
        try:
            result = subprocess.run(
                ["adb"] + list(args),
                capture_output=True, text=True, timeout=timeout
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return ""

    def get_current_activity(self) -> str:
        out = self.adb("dumpsys", "window", "displays")
        for line in out.splitlines():
            if "mCurrentFocus" in line or "mFocusedApp" in line:
                match = re.search(r'(\S+/\S+)\}', line)
                if match:
                    return match.group(1)
        return "unknown"

    def dump_ui(self) -> Optional[ET.Element]:
        self.adb("uiautomator", "dump", "/sdcard/ui_dump.xml")
        self.adb_host("pull", "/sdcard/ui_dump.xml", self.dump_file)
        try:
            tree = ET.parse(self.dump_file)
            return tree.getroot()
        except ET.ParseError:
            return None

    def screenshot(self, name: str) -> str:
        filename = f"{name}.png"
        filepath = os.path.join(self.output_dir, filename)
        self.adb("screencap", "-p", "/sdcard/adb_screen.png")
        self.adb_host("pull", "/sdcard/adb_screen.png", filepath)
        return filename

    def tap(self, x: int, y: int):
        self.adb("input", "tap", str(x), str(y))

    def go_back(self):
        self.adb("input", "keyevent", "KEYCODE_BACK")

    def hide_keyboard(self):
        # Check if keyboard is shown
        out = self.adb("dumpsys", "input_method")
        if "mInputShown=true" in out:
            self.go_back()
            time.sleep(0.5)

    def is_in_app(self) -> bool:
        return self.package in self.get_current_activity()

    # --- Element analysis ---

    def get_label(self, node: ET.Element) -> str:
        t = node.get("text", "")
        if t:
            return t
        d = node.get("content-desc", "")
        if d:
            return d.split("\n")[0]
        rid = node.get("resource-id", "")
        if rid:
            return rid.split("/")[-1]
        for child in node.iter("node"):
            if child is node:
                continue
            ct = child.get("text", "")
            if ct:
                return ct
            cd = child.get("content-desc", "")
            if cd:
                return cd.split("\n")[0]
        return "(unknown)"

    def parse_bounds(self, bounds_str: str):
        m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", bounds_str)
        if not m:
            return None
        x1, y1, x2, y2 = int(m[1]), int(m[2]), int(m[3]), int(m[4])
        return x1, y1, x2, y2, (x1 + x2) // 2, (y1 + y2) // 2

    def is_input_element(self, node: ET.Element) -> bool:
        """Check if element is a text input field."""
        cls = node.get("class", "")
        if cls in INPUT_CLASSES:
            return True
        rid = node.get("resource-id", "").lower()
        if any(p in rid for p in INPUT_ID_PATTERNS):
            return True
        # Check if it has hint text or is focusable with editable parent
        if node.get("password") == "true":
            return True
        return False

    def classify_elements(self, root: ET.Element) -> list:
        """Extract and classify all clickable elements."""
        elements = []
        idx = 0
        for node in root.iter("node"):
            if node.get("clickable") != "true":
                continue
            bounds_str = node.get("bounds", "")
            parsed = self.parse_bounds(bounds_str)
            if not parsed:
                continue
            x1, y1, x2, y2, cx, cy = parsed

            # classify
            if self.is_input_element(node):
                etype = "input"
            else:
                etype = "unknown"  # will be determined after clicking

            elements.append(ClickableElement(
                index=idx,
                label=self.get_label(node),
                class_name=node.get("class", ""),
                resource_id=node.get("resource-id", ""),
                center=(cx, cy),
                bounds=(x1, y1, x2, y2),
                element_type=etype,
            ))
            idx += 1
        return elements

    # --- Page fingerprinting ---

    def get_content_fingerprint(self, root: ET.Element) -> str:
        """Fingerprint based on ALL visible text content (not just clickables)."""
        texts = []
        for node in root.iter("node"):
            t = node.get("text", "")
            if t:
                texts.append(t)
            d = node.get("content-desc", "")
            if d:
                texts.append(d.split("\n")[0])
        content = "|".join(texts)
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def get_activity_key(self, activity: str) -> str:
        """Normalize activity name for comparison."""
        if "/" in activity:
            return activity.split("/")[-1].lstrip(".")
        return activity

    def get_page_title(self, root: ET.Element, activity: str) -> str:
        for node in root.iter("node"):
            rid = node.get("resource-id", "")
            if any(k in rid for k in ["toolbar", "title", "action_bar"]):
                t = node.get("text", "")
                if t:
                    return t
        if "/" in activity:
            return activity.split("/")[-1].lstrip(".")
        return activity

    # --- Core exploration ---

    def explore(self, depth: int = 0, path_prefix: str = "0") -> Optional[PageNode]:
        """Explore current page: classify elements, handle tabs/nav/input differently."""
        if depth > self.max_depth:
            print(f"{'  ' * depth}⏹ Max depth {self.max_depth} reached")
            return None

        root = self.dump_ui()
        if root is None:
            print(f"{'  ' * depth}⚠ UI dump failed")
            return None

        activity = self.get_current_activity()
        activity_key = self.get_activity_key(activity)
        content_fp = self.get_content_fingerprint(root)
        page_key = f"{activity_key}:{content_fp}"

        # Dedup by activity + content
        if page_key in self.visited_pages:
            print(f"{'  ' * depth}⟳ Already visited: {activity_key}")
            return None
        self.visited_pages.add(page_key)

        # Screenshot current page
        title = self.get_page_title(root, activity)
        safe_title = re.sub(r'[^\w\-]', '_', title)[:30]
        screenshot_name = f"{path_prefix}_{safe_title}"
        screenshot_file = self.screenshot(screenshot_name)

        elements = self.classify_elements(root)
        print(f"{'  ' * depth}📄 [{path_prefix}] {title} ({len(elements)} clickable)")

        page = PageNode(
            page_id=page_key,
            activity=activity,
            title=title,
            screenshot=screenshot_file,
            clickables=[f"[{e.element_type}] {e.label}" for e in elements],
        )

        # Process each element
        for i, elem in enumerate(elements):
            child_prefix = f"{path_prefix}.{i}"

            # Skip input fields
            if elem.element_type == "input":
                print(f"{'  ' * depth}  ⌨ [{child_prefix}] skip input: {elem.label}")
                continue

            print(f"{'  ' * depth}  → [{child_prefix}] tap: {elem.label}")

            # Remember state before tap
            pre_activity = activity

            self.tap(elem.center[0], elem.center[1])
            time.sleep(self.wait_after_tap)

            # Hide keyboard if it popped up (input field we didn't catch)
            self.hide_keyboard()

            # Check what happened
            if not self.is_in_app():
                print(f"{'  ' * depth}    ⚠ Left app, going back")
                self.go_back()
                time.sleep(self.wait_after_back)
                if not self.is_in_app():
                    self.adb("monkey", "-p", self.package,
                             "-c", "android.intent.category.LAUNCHER", "1")
                    time.sleep(3)
                continue

            new_root = self.dump_ui()
            if new_root is None:
                self.go_back()
                time.sleep(self.wait_after_back)
                continue

            new_activity = self.get_current_activity()
            new_activity_key = self.get_activity_key(new_activity)
            new_content_fp = self.get_content_fingerprint(new_root)

            # --- Classify what happened ---

            if new_content_fp == content_fp:
                # Nothing changed
                print(f"{'  ' * depth}    (no change)")
                continue

            if new_activity_key != self.get_activity_key(pre_activity):
                # NAVIGATE: different activity → explore recursively, then BACK
                print(f"{'  ' * depth}    📱 navigate → {new_activity_key}")
                child_page = self.explore(depth + 1, child_prefix)
                if child_page:
                    page.children.append({
                        "type": "navigate",
                        "clicked": elem.label,
                        "page": child_page,
                    })
                # Go back
                self._return_to_page(pre_activity)

            else:
                # TAB: same activity, content changed → screenshot & record, NO back
                tab_key = f"{new_activity_key}:{new_content_fp}"
                if tab_key not in self.visited_tabs:
                    self.visited_tabs.add(tab_key)
                    tab_title = f"{elem.label}"
                    safe_tab = re.sub(r'[^\w\-]', '_', tab_title)[:30]
                    tab_screenshot = self.screenshot(f"{child_prefix}_tab_{safe_tab}")
                    new_elements = self.classify_elements(new_root)
                    print(f"{'  ' * depth}    🏷 tab: {elem.label} ({len(new_elements)} clickable)")
                    page.tabs.append({
                        "type": "tab",
                        "clicked": elem.label,
                        "screenshot": tab_screenshot,
                        "clickables": [f"[{e.element_type}] {e.label}" for e in new_elements],
                    })
                else:
                    print(f"{'  ' * depth}    🏷 tab: {elem.label} (already seen)")

        return page

    def _return_to_page(self, target_activity: str):
        """Try to return to the target activity."""
        target_key = self.get_activity_key(target_activity)
        for attempt in range(4):
            self.go_back()
            time.sleep(self.wait_after_back)
            current = self.get_current_activity()
            if target_key in self.get_activity_key(current):
                return True
            if not self.is_in_app():
                # Re-launch app
                self.adb("monkey", "-p", self.package,
                         "-c", "android.intent.category.LAUNCHER", "1")
                time.sleep(3)
                return False
        return False

    # --- Entry point ---

    def run(self):
        print(f"🚀 Exploring: {self.package}")
        print(f"📁 Output: {self.output_dir}")
        print(f"📏 Max depth: {self.max_depth}")
        print()

        # Launch app
        self.adb("monkey", "-p", self.package,
                 "-c", "android.intent.category.LAUNCHER", "1")
        time.sleep(3)

        tree = self.explore()

        if tree is None:
            print("\n⚠ No pages explored")
            return

        self._save_tree_json(tree)
        self._save_tree_markdown(tree)

        total = len(self.visited_pages) + len(self.visited_tabs)
        print(f"\n✅ Done! {len(self.visited_pages)} pages + {len(self.visited_tabs)} tabs explored")
        print(f"   📄 {self.output_dir}/tree.json")
        print(f"   📝 {self.output_dir}/tree.md")

    # --- Output ---

    def _page_to_dict(self, page: PageNode) -> dict:
        return {
            "page_id": page.page_id,
            "activity": page.activity,
            "title": page.title,
            "screenshot": page.screenshot,
            "clickables": page.clickables,
            "tabs": page.tabs,
            "children": [
                {
                    "type": c["type"],
                    "clicked": c["clicked"],
                    "page": self._page_to_dict(c["page"]),
                }
                for c in page.children
            ],
        }

    def _save_tree_json(self, tree: PageNode):
        data = self._page_to_dict(tree)
        path = os.path.join(self.output_dir, "tree.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _save_tree_markdown(self, tree: PageNode, f=None, depth=0):
        if f is None:
            path = os.path.join(self.output_dir, "tree.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write("# App Exploration Tree\n\n")
                f.write(f"Package: `{self.package}`\n\n")
                self._save_tree_markdown(tree, f, 0)
            return

        indent = "  " * depth
        f.write(f"{indent}- **{tree.title}** ({len(tree.clickables)} clickable)\n")
        f.write(f"{indent}  - Activity: `{tree.activity}`\n")
        f.write(f"{indent}  - Screenshot: `{tree.screenshot}`\n")
        f.write(f"{indent}  - Elements: {', '.join(tree.clickables[:8])}")
        if len(tree.clickables) > 8:
            f.write(f" ... +{len(tree.clickables) - 8} more")
        f.write("\n")

        # Tabs
        for tab in tree.tabs:
            f.write(f"{indent}  - 🏷 **tab: {tab['clicked']}** → `{tab['screenshot']}`\n")
            f.write(f"{indent}    - Elements: {', '.join(tab['clickables'][:6])}")
            if len(tab['clickables']) > 6:
                f.write(f" ... +{len(tab['clickables']) - 6} more")
            f.write("\n")

        # Navigation children
        for child in tree.children:
            f.write(f"{indent}  - 📱 **navigate: {child['clicked']}** →\n")
            self._save_tree_markdown(child["page"], f, depth + 2)


def main():
    parser = argparse.ArgumentParser(description="Explore Android app UI via ADB")
    parser.add_argument("package", help="App package name")
    parser.add_argument("--depth", type=int, default=3, help="Max depth (default: 3)")
    parser.add_argument("--output", default="./explore_output", help="Output directory")
    parser.add_argument("--wait-tap", type=float, default=2.0, help="Wait after tap (s)")
    parser.add_argument("--wait-back", type=float, default=1.0, help="Wait after back (s)")
    args = parser.parse_args()

    explorer = AppExplorer(
        package=args.package,
        output_dir=args.output,
        max_depth=args.depth,
        wait_after_tap=args.wait_tap,
        wait_after_back=args.wait_back,
    )
    explorer.run()


if __name__ == "__main__":
    main()
