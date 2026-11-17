#!/usr/bin/env python3
"""Self-test for fit_checker.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fit_checker import (to_cm, parse_dims, check_door, check_corner,
                         check_stairs, check_room, floorplan)


def test_units():
    assert abs(to_cm("86in") - 218.44) < 0.01
    assert abs(to_cm("14ft") - 426.72) < 0.01
    assert abs(to_cm("203cm") - 203) < 0.01
    assert abs(to_cm("1.2m") - 120) < 0.01
    assert abs(to_cm("86") - 218.44) < 0.01  # plain = inches
    try:
        to_cm("banana")
        assert False
    except ValueError:
        pass
    print("ok units")


def test_dims():
    w, d, h = parse_dims("86x37x35in")
    assert abs(w - 218.44) < 0.1 and abs(h - 88.9) < 0.1
    print("ok dims")


def test_door():
    # small box through big door: fits
    r = check_door((60, 40, 30), 90, 200)
    assert r["fits"], r["detail"]
    # huge sofa (218×94×89cm) through a 81×203cm apartment door: FAILS
    # cross-sections: 89×94 (no), 89×218 (no), 94×218 (no) — tilt can't save it
    r = check_door((218, 94, 89), 81, 203)
    assert not r["fits"]
    # wardrobe 120×60×200 through 100×210 door: travel = height(200),
    # cross-section 120×60 -> 60<=100, 120<=210 ✓ fits (carried upright lying on side)
    r = check_door((120, 60, 200), 100, 210)
    assert r["fits"]
    # same wardrobe through a lower 100×190 door: no orientation works
    # (cross 200×60 needs height>=200; 120×60 needs width>=120; 200×120 needs
    #  width>=120) — tilt check: 60×200 diagonal 208.8 > door diag 212.8? no wait
    # opening diag = sqrt(100²+190²)=214.9 >= 208.8 → tilted fits! Hmm — the
    # tilt rule is diagonal-of-opening vs diagonal-of-cross-section ONLY when
    # the smaller cross dim fits the opening width. 60<=100 ✓ so tilted passes.
    r = check_door((120, 60, 200), 100, 190)
    assert r["fits"], "tilt through tall-narrow should pass"  # corrected expectation
    # a genuinely impossible case: long rigid pole through small door
    r = check_door((300, 20, 20), 80, 200)
    # cross 20×300: 20<=80 but 300>200; tilt: diag 300.7 > opening diag 215? fail
    # cross 20×20 fits trivially? NO — travel would be 300 (the pole length IS
    # the travel direction), cross-section 20×20 <= 80×200 ✓ PASSES straight through
    assert r["fits"], "pole goes through lengthwise"
    print("ok door checks")


def test_corner():
    # 2m pole down 1m corridors at right angle: impossible
    r = check_corner((200, 10, 10), 100, 100)
    assert not r["fits"]
    # 90cm item around 120cm corridors: fine
    r = check_corner((90, 40, 40), 120, 120)
    assert r["fits"] and r["angle_range_deg"] is not None
    print(f"ok corner: min widths {r['min_hall_a_needed_cm']:.0f}/{r['min_hall_b_needed_cm']:.0f}cm")


def test_stairs():
    # rigid box spring 193×91×23 up a 105cm-wide stair with 200cm headroom:
    # travel=91, cross 23×193 -> 23<=105, 193<=200 ✓ fits
    r = check_stairs((193, 91, 23), 105, headroom=200)
    assert r["fits"]
    # same with low 150cm headroom: 23×193 needs headroom>=193 fail; 23×91
    # needs width... travel=193, cross 23×91: 23<=105 and 91<=150 ✓ still fits
    r = check_stairs((193, 91, 23), 105, headroom=150)
    assert r["fits"]
    # tall wardrobe: no orientation works with tight width+headroom
    r = check_stairs((100, 55, 205), 110, headroom=190)
    # cross 55×205 needs 205<=190 fail; travel=205 cross 55×100: 55<=110,
    # 100<=190 ✓ fits lying down
    assert r["fits"], "wardrobe lies down"
    # truly impossible: big cube in narrow stairs with low headroom
    r = check_stairs((180, 170, 160), 100, headroom=150)
    assert not r["fits"]
    print("ok stairs")


def test_room():
    # 213cm sofa in 4.3x3.35m room against long wall
    r = check_room(213, 94, 430, 335, wall="long")
    assert r["walkway_cm"] == 335 - 94
    assert r["walkway_ok"] and r["fits"]
    # same sofa in a narrow 160cm-deep room: walkway 66cm fails
    r = check_room(213, 94, 430, 160, wall="long")
    assert r["walkway_cm"] == 66 and not r["walkway_ok"] and not r["fits"]
    # item longer than wall
    r = check_room(250, 100, 200, 300, wall="long")
    assert not r["fits"] and any("wall" in i for i in r["issues"])
    # opposite furniture eats walkway
    r = check_room(150, 60, 400, 300, wall="long", other=[(120, 60)])
    # gap = 300-60-60 = 180 >= 75 -> ok
    assert r["fits"]
    r = check_room(150, 60, 400, 190, wall="long", other=[(120, 60)])
    # gap = 190-60-60 = 70 < 75 -> fails
    assert not r["fits"]
    print("ok room checks")


def test_floorplan():
    out = floorplan(430, 335, 213, 94, wall="long", other=[(150, 60)])
    assert isinstance(out, str) and "|" in out and "#" in out
    lines = out.splitlines()
    assert len(lines) > 8
    print("ok floorplan renders")


if __name__ == "__main__":
    test_units()
    test_dims()
    test_door()
    test_corner()
    test_stairs()
    test_room()
    test_floorplan()
    print("\nALL TESTS PASSED ✅")
