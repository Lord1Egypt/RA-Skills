#!/usr/bin/env python3
"""Desktop Pilot - Linux accessibility helper (AT-SPI). Needs python3-gi + gir1.2-atspi-2.0 (preinstalled on GNOME/KDE desktops).
Usage: atspi.py buttons|click|close --app NAME [--title T] [--name LABEL]"""
import argparse
import sys

import gi

gi.require_version("Atspi", "2.0")
from gi.repository import Atspi  # noqa: E402

CLICKABLE = {"push button", "toggle button", "menu item", "check box", "radio button", "link", "page tab", "combo box"}


def apps(name):
    desk = Atspi.get_desktop(0)
    for i in range(desk.get_child_count()):
        a = desk.get_child_at_index(i)
        if a and (not name or name.lower() in (a.get_name() or "").lower()):
            yield a


def frames(name, title):
    for a in apps(name):
        for i in range(a.get_child_count()):
            w = a.get_child_at_index(i)
            if w and (not title or title in (w.get_name() or "")):
                yield w


def walk(node, depth=0):
    if node is None or depth > 40:
        return
    yield node
    for i in range(node.get_child_count()):
        yield from walk(node.get_child_at_index(i), depth + 1)


def press(el):
    act = el.get_action_iface()
    if act:
        for i in range(act.get_n_actions()):
            if act.get_action_name(i) in ("click", "press", "activate", "toggle", "jump"):
                return act.do_action(i)
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["buttons", "click", "close"])
    p.add_argument("--app")
    p.add_argument("--title")
    p.add_argument("--name")
    a = p.parse_args()
    wins = list(frames(a.app, a.title))
    if not wins:
        sys.exit("No accessible window matches (is the app running with accessibility enabled?)")
    if a.action == "buttons":
        for w in wins:
            print(f"[window] {w.get_name()}")
            for el in walk(w):
                if el.get_role_name() in CLICKABLE and el.get_name():
                    print(f"  {el.get_role_name()}\t{el.get_name()}")
        return
    if a.action == "close":
        names = {"close", "cerrar", "fermer", "schließen", "chiudi"}
        for el in walk(wins[0]):
            if el.get_role_name() == "push button" and (el.get_name() or "").lower() in names and press(el):
                print(f"OK closed '{wins[0].get_name()}'")
                return
        sys.exit("No close button exposed; use the window manager fallback")
    if not a.name:
        sys.exit("Specify --name <visible label>")
    for w in wins:
        for el in walk(w):
            if el.get_name() == a.name and press(el):
                print(f"OK clicked '{a.name}'")
                return
    sys.exit(f"Control not found: '{a.name}' (run 'buttons' to list exact labels)")


if __name__ == "__main__":
    main()
