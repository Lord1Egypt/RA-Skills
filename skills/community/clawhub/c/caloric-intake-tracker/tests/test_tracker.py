import sqlite3
import pytest
from pathlib import Path
from datetime import date, timedelta
from scripts.tracker import init_db, get_db, get_goal, get_valid_meal_types, validate_meal_type

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_health_data.db"
    init_db(db_file)
    return db_file

def test_database_init(temp_db):
    conn = get_db(temp_db)
    # Check if all tables exist
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t['name'] for t in tables]
    
    assert "entries" in table_names
    assert "daily_goal" in table_names
    assert "weight_log" in table_names
    assert "measurement_types" in table_names
    assert "measurement_log" in table_names
    assert "day_notes" in table_names
    assert "meal_types" in table_names
    
    # Check if body_measurements exists as a view
    views = conn.execute("SELECT name FROM sqlite_master WHERE type='view'").fetchall()
    view_names = [v['name'] for v in views]
    assert "body_measurements" in view_names
    
    # Check if 'completed' column exists in day_notes
    columns = conn.execute("PRAGMA table_info(day_notes)").fetchall()
    col_names = [c['name'] for c in columns]
    assert "completed" in col_names
    
    conn.close()

def test_meal_types_seeding(temp_db):
    valid_meals = get_valid_meal_types(temp_db)
    assert "breakfast" in valid_meals
    assert "lunch" in valid_meals
    assert "dinner" in valid_meals
    assert "snack" in valid_meals

def test_goal_setting_calorie_only(temp_db):
    conn = get_db(temp_db)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO daily_goal (id, calorie_goal, protein_goal) VALUES (1, 2000, NULL)")
    conn.commit()
    conn.close()
    
    cal, p, h = get_goal(temp_db)
    assert cal == 2000
    assert p is None

def test_goal_setting_with_protein(temp_db):
    conn = get_db(temp_db)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO daily_goal (id, calorie_goal, protein_goal) VALUES (1, 1800, 120.5)")
    conn.commit()
    conn.close()
    
    cal, p, h = get_goal(temp_db)
    assert cal == 1800
    assert p == 120.5

def test_harmonized_cli_feedback(temp_db, capsys):
    import argparse
    from scripts.tracker import cmd_add, cmd_update, cmd_delete
    
    # Set goal first
    conn = get_db(temp_db)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO daily_goal (id, calorie_goal, protein_goal) VALUES (1, 1800, 120)")
    conn.commit()
    conn.close()
    
    # Add first entry
    add_args = argparse.Namespace(
        database=str(temp_db),
        food_name="Breakfast",
        calories=350,
        protein=20.0,
        carbs=30.0,
        fat=10.0,
        meal="breakfast",
        date="2026-06-15"
    )
    cmd_add(add_args)
    captured = capsys.readouterr()
    assert "Added Entry 1: +350 (350/1800)\n" in captured.out
    
    # Add second entry
    add_args2 = argparse.Namespace(
        database=str(temp_db),
        food_name="Lunch",
        calories=600,
        protein=30.0,
        carbs=50.0,
        fat=15.0,
        meal="lunch",
        date="2026-06-15"
    )
    cmd_add(add_args2)
    captured = capsys.readouterr()
    assert "Added Entry 2: +600 (950/1800)\n" in captured.out
    
    # Update first entry
    update_args = argparse.Namespace(
        database=str(temp_db),
        id=1,
        name=None,
        cal=400,
        p=None,
        c=None,
        f=None,
        meal=None
    )
    cmd_update(update_args)
    captured = capsys.readouterr()
    assert "Changed Entry 1: 350->400 (1000/1800)\n" in captured.out
    
    # Delete first entry
    delete_args = argparse.Namespace(
        database=str(temp_db),
        id=1
    )
    cmd_delete(delete_args)
    captured = capsys.readouterr()
    assert "Deleted Entry 1: -400 (600/1800)\n" in captured.out


def test_search_command(temp_db, capsys):
    import argparse
    from scripts.tracker import cmd_add, cmd_search
    
    # 1. Add some entries for search testing
    # Entry 1: Oatmeal (logged 2x)
    add_args1 = argparse.Namespace(
        database=str(temp_db),
        food_name="Oatmeal with blueberries",
        calories=350,
        protein=12.0,
        carbs=50.0,
        fat=5.0,
        meal="breakfast",
        date="2026-06-14"
    )
    cmd_add(add_args1)
    
    add_args2 = argparse.Namespace(
        database=str(temp_db),
        food_name="Oatmeal with blueberries",
        calories=350,
        protein=12.0,
        carbs=50.0,
        fat=5.0,
        meal="breakfast",
        date="2026-06-15"
    )
    cmd_add(add_args2)
    
    # Entry 2: Chicken Salad (logged 1x)
    add_args3 = argparse.Namespace(
        database=str(temp_db),
        food_name="Grilled chicken salad",
        calories=450,
        protein=40.0,
        carbs=10.0,
        fat=15.0,
        meal="lunch",
        date="2026-06-15"
    )
    cmd_add(add_args3)
    
    # Clear capture
    capsys.readouterr()
    
    # 2. Test exact/substring search
    search_args_sub = argparse.Namespace(
        database=str(temp_db),
        query="oat",
        limit=5
    )
    cmd_search(search_args_sub)
    captured = capsys.readouterr()
    assert "Found 1 similar registered food(s):" in captured.out
    assert "Oatmeal with blueberries (350 kcal) - breakfast" in captured.out
    assert "Logged 2x (last used: 2026-06-15)" in captured.out
    assert "Log command: python scripts/tracker.py add \"Oatmeal with blueberries\" 350 12.0 50.0 5.0 --meal breakfast" in captured.out

    # 3. Test fuzzy search (e.g. typing "otmel")
    search_args_fuzzy = argparse.Namespace(
        database=str(temp_db),
        query="otmel",
        limit=5
    )
    cmd_search(search_args_fuzzy)
    captured = capsys.readouterr()
    assert "Found 1 similar registered food(s):" in captured.out
    assert "Oatmeal with blueberries (350 kcal) - breakfast" in captured.out

    # 4. Test no results found
    search_args_none = argparse.Namespace(
        database=str(temp_db),
        query="pizza",
        limit=5
    )
    cmd_search(search_args_none)
    captured = capsys.readouterr()
    assert "No similar registered foods found for 'pizza'" in captured.out


def test_stats_today(temp_db, capsys):
    import argparse
    from scripts.tracker import cmd_add, cmd_goal, cmd_weight, cmd_waist, cmd_stats_day, cmd_stats_week, cmd_stats_trend, cmd_stats_weight, cmd_stats_waist

    # 1. Set goal
    goal_args = argparse.Namespace(
        database=str(temp_db),
        calories=1800,
        protein=100.0,
        height=180.0
    )
    cmd_goal(goal_args)

    # 2. Add some entries
    # Monday 2026-06-15
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Egg", calories=100, protein=10.0, carbs=1.0, fat=8.0, meal="breakfast", date="2026-06-15", today=None
    ))
    # Tuesday 2026-06-16
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Chicken", calories=500, protein=50.0, carbs=0.0, fat=10.0, meal="lunch", date="2026-06-16", today=None
    ))
    # Wednesday 2026-06-17
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Fish", calories=400, protein=40.0, carbs=2.0, fat=12.0, meal="dinner", date="2026-06-17", today=None
    ))
    # Thursday 2026-06-18
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Steak", calories=800, protein=60.0, carbs=0.0, fat=40.0, meal="dinner", date="2026-06-18", today=None
    ))

    # Log weights
    cmd_weight(argparse.Namespace(database=str(temp_db), kg=80.0, date="2026-06-15", today=None))
    cmd_weight(argparse.Namespace(database=str(temp_db), kg=79.5, date="2026-06-17", today=None))
    cmd_weight(argparse.Namespace(database=str(temp_db), kg=79.0, date="2026-06-19", today=None))

    # Log waists
    cmd_waist(argparse.Namespace(database=str(temp_db), cm=90.0, date="2026-06-15", today=None))
    cmd_waist(argparse.Namespace(database=str(temp_db), cm=89.5, date="2026-06-17", today=None))
    cmd_waist(argparse.Namespace(database=str(temp_db), cm=89.0, date="2026-06-19", today=None))

    # Clear capture
    capsys.readouterr()

    # 3. Test stats day --today 2026-06-16
    day_args = argparse.Namespace(database=str(temp_db), date=None, today="2026-06-16", no_group=True)
    cmd_stats_day(day_args)
    captured = capsys.readouterr()
    assert "DAY BREAKDOWN: 2026-06-16" in captured.out
    assert "Chicken" in captured.out

    # 4. Test stats week --today 2026-06-17 (Wednesday)
    # The week containing June 17 has Monday=June 15, Sunday=June 21.
    # It should only show logs up to June 17. June 18 (Steak) should be ignored.
    week_args = argparse.Namespace(database=str(temp_db), date=None, weeks=1, compact=False, today="2026-06-17")
    cmd_stats_week(week_args)
    captured = capsys.readouterr()
    # Wednesday 2026-06-17 should be visible, Thursday 2026-06-18 should be UNLOGGED
    assert "Wednesday  | 2026-06-17 | 400" in captured.out
    assert "Thursday   | 2026-06-18 | -" in captured.out
    # Total should only sum up to Wednesday (100+500+400 = 1000)
    assert "Total: 1000 / 12600 kcal" in captured.out

    # 5. Test stats trend --today 2026-06-17
    trend_args = argparse.Namespace(database=str(temp_db), days=30, today="2026-06-17")
    cmd_stats_trend(trend_args)
    captured = capsys.readouterr()
    # Average of last 7 days including up to June 17:
    # Entries: June 15 (100 kcal), June 16 (500 kcal), June 17 (400 kcal)
    # Total calories = 1000. Under rolling trend, the rolling average for June 17 should be calculated.
    assert "Last  7 Days:" in captured.out

    # 6. Test stats weight --today 2026-06-17
    weight_args = argparse.Namespace(database=str(temp_db), days=30, entries=None, today="2026-06-17")
    cmd_stats_weight(weight_args)
    captured = capsys.readouterr()
    # Weight on June 19 (79.0) should NOT be shown
    assert "2026-06-17: 79.5 kg" in captured.out
    assert "2026-06-19" not in captured.out

    # 7. Test stats waist --today 2026-06-17
    waist_args = argparse.Namespace(database=str(temp_db), days=30, entries=None, today="2026-06-17")
    cmd_stats_waist(waist_args)
    captured = capsys.readouterr()
    # Waist on June 19 (89.0) should NOT be shown
    assert "2026-06-17: 89.5 cm" in captured.out
    assert "2026-06-19" not in captured.out


def test_stats_weight_and_waist_entries(temp_db, capsys):
    import argparse
    from scripts.tracker import cmd_weight, cmd_waist, cmd_stats_weight, cmd_stats_waist, entries_type
    import pytest

    # Log 6 weights/waists
    dates = ["2026-06-10", "2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15"]
    weights = [80.0, 79.8, 79.5, 79.6, 79.2, 79.0]
    for d, w in zip(dates, weights):
        cmd_weight(argparse.Namespace(database=str(temp_db), kg=w, date=d, today=None))
        cmd_waist(argparse.Namespace(database=str(temp_db), cm=90.0 - (80.0 - w), date=d, today=None))

    # Clear capture
    capsys.readouterr()

    # Case 1: Default (neither entries nor days specified -> entries=5)
    args_def = argparse.Namespace(database=str(temp_db), entries=None, days=None, today="2026-06-15")
    cmd_stats_weight(args_def)
    out = capsys.readouterr().out
    assert "WEIGHT TRENDS (LAST 5 ENTRIES)" in out
    # Verify formatting (diff right after kg, before BMI)
    assert "2026-06-15: 79.0 kg (-0.2 kg) | BMI: N/A" in out
    assert "2026-06-11: 79.8 kg (-0.2 kg) | BMI: N/A" in out
    # Verify chronological order (oldest first, newest last)
    idx_old = out.find("2026-06-11")
    idx_new = out.find("2026-06-15")
    assert idx_old < idx_new
    assert "2026-06-10" not in out # The 6th entry should be excluded

    # Case 2: Explicit entries (-N 3)
    args_n3 = argparse.Namespace(database=str(temp_db), entries=3, days=None, today="2026-06-15")
    cmd_stats_weight(args_n3)
    out = capsys.readouterr().out
    assert "WEIGHT TRENDS (LAST 3 ENTRIES)" in out
    assert "2026-06-15: 79.0 kg (-0.2 kg) | BMI: N/A" in out
    assert "2026-06-13: 79.6 kg (+0.1 kg) | BMI: N/A" in out
    # Verify order
    idx_old = out.find("2026-06-13")
    idx_new = out.find("2026-06-15")
    assert idx_old < idx_new
    assert "2026-06-12" not in out

    # Case 3: Explicit entries "all" (-N all)
    args_all = argparse.Namespace(database=str(temp_db), entries="all", days=None, today="2026-06-15")
    cmd_stats_weight(args_all)
    out = capsys.readouterr().out
    assert "WEIGHT TRENDS (ALL ENTRIES)" in out
    assert "2026-06-15: 79.0 kg (-0.2 kg) | BMI: N/A" in out
    assert "2026-06-10: 80.0 kg | BMI: N/A" in out # oldest has no diff
    idx_old = out.find("2026-06-10")
    idx_new = out.find("2026-06-15")
    assert idx_old < idx_new

    # Case 4: Only days specified (--days 3 -> should not limit entries count)
    args_days3 = argparse.Namespace(database=str(temp_db), entries=None, days=3, today="2026-06-15")
    cmd_stats_weight(args_days3)
    out = capsys.readouterr().out
    assert "WEIGHT TRENDS (LAST 3 DAYS)" in out
    assert "2026-06-15: 79.0 kg (-0.2 kg) | BMI: N/A" in out
    assert "2026-06-12: 79.5 kg (-0.3 kg) | BMI: N/A" in out
    assert "2026-06-11" not in out

    # Case 5: Both entries and days specified (-N 2 --days 5)
    args_both = argparse.Namespace(database=str(temp_db), entries=2, days=5, today="2026-06-15")
    cmd_stats_weight(args_both)
    out = capsys.readouterr().out
    assert "WEIGHT TRENDS (LAST 2 ENTRIES OVER LAST 5 DAYS)" in out
    assert "2026-06-15: 79.0 kg (-0.2 kg) | BMI: N/A" in out
    assert "2026-06-14: 79.2 kg (-0.4 kg) | BMI: N/A" in out
    assert "2026-06-13" not in out

    # Case 6: Custom entries validator validation
    assert entries_type("all") == "all"
    assert entries_type("ALL") == "all"
    assert entries_type("5") == 5
    with pytest.raises(argparse.ArgumentTypeError):
        entries_type("0")
    with pytest.raises(argparse.ArgumentTypeError):
        entries_type("-1")
    with pytest.raises(argparse.ArgumentTypeError):
        entries_type("abc")


def test_cmd_list_and_stats_day_default_grouping_and_no_group(temp_db, capsys):
    import argparse
    from scripts.tracker import cmd_add, cmd_list, cmd_stats_day

    # 1. Add some entries for testing
    # Lunch entries
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Apple", calories=60, protein=1.0, carbs=15.0, fat=0.2, meal="lunch", date="2026-06-20", today=None
    ))
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Banana", calories=100, protein=1.3, carbs=23.0, fat=0.3, meal="lunch", date="2026-06-20", today=None
    ))
    # Dinner entries
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Steak", calories=500, protein=40.0, carbs=0.0, fat=35.0, meal="dinner", date="2026-06-20", today=None
    ))
    cmd_add(argparse.Namespace(
        database=str(temp_db), food_name="Broccoli", calories=40, protein=None, carbs=6.0, fat=0.0, meal="dinner", date="2026-06-20", today=None
    ))

    # Clear captured output
    capsys.readouterr()

    # 2. Test cmd_list default grouping
    list_args = argparse.Namespace(database=str(temp_db), date="2026-06-20", no_group=False, today=None)
    cmd_list(list_args)
    captured = capsys.readouterr().out
    assert "Entries for 2026-06-20:" in captured
    assert "  • lunch: Apple, Banana — 160 kcal | 2.3g P" in captured
    assert "  • dinner: Steak, Broccoli — 540 kcal | 40.0g P" in captured

    # 3. Test cmd_list --no-group fallback
    list_args_no_group = argparse.Namespace(database=str(temp_db), date="2026-06-20", no_group=True, today=None)
    cmd_list(list_args_no_group)
    captured_raw = capsys.readouterr().out
    assert "Entries for 2026-06-20:" in captured_raw
    assert "[1]" in captured_raw and "[lunch] Apple: 60 kcal | 1.0g P" in captured_raw
    assert "[2]" in captured_raw and "[lunch] Banana: 100 kcal | 1.3g P" in captured_raw
    assert "[3]" in captured_raw and "[dinner] Steak: 500 kcal | 40.0g P" in captured_raw
    assert "[4]" in captured_raw and "[dinner] Broccoli: 40 kcal" in captured_raw

    # 4. Test cmd_stats_day default grouping
    stats_args = argparse.Namespace(database=str(temp_db), date="2026-06-20", no_group=False, today=None)
    cmd_stats_day(stats_args)
    captured_stats = capsys.readouterr().out
    assert "DAY BREAKDOWN: 2026-06-20" in captured_stats
    assert "  • lunch: Apple, Banana — 160 kcal, 2g P" in captured_stats
    assert "  • dinner: Steak, Broccoli — 540 kcal, 40g P" in captured_stats

    # 5. Test cmd_stats_day --no-group fallback
    stats_args_no_group = argparse.Namespace(database=str(temp_db), date="2026-06-20", no_group=True, today=None)
    cmd_stats_day(stats_args_no_group)
    captured_stats_raw = capsys.readouterr().out
    assert "DAY BREAKDOWN: 2026-06-20" in captured_stats_raw
    assert "[1]" in captured_stats_raw and "[lunch] Apple: 60 kcal, 1g P" in captured_stats_raw
    assert "[2]" in captured_stats_raw and "[lunch] Banana: 100 kcal, 1g P" in captured_stats_raw
    assert "[3]" in captured_stats_raw and "[dinner] Steak: 500 kcal, 40g P" in captured_stats_raw
    assert "[4]" in captured_stats_raw and "[dinner] Broccoli: 40 kcal" in captured_stats_raw


def test_legacy_database_migration(tmp_path):
    import sqlite3
    from scripts.tracker import init_db
    
    db_file = tmp_path / "legacy_test.db"
    
    # 1. Create legacy schema
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE body_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            waist_cm REAL,
            hips_cm REAL,
            neck_cm REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute("INSERT INTO body_measurements (date, waist_cm, hips_cm, neck_cm) VALUES ('2026-06-01', 90.0, 100.0, 38.0)")
    c.execute("INSERT INTO body_measurements (date, waist_cm, hips_cm, neck_cm) VALUES ('2026-06-02', 89.5, 99.5, NULL)")
    conn.commit()
    conn.close()
    
    # 2. Run init_db which triggers migration
    init_db(db_file)
    
    # 3. Connect and verify migrated values
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Check if view body_measurements works
    rows = c.execute("SELECT date, waist_cm, hips_cm, neck_cm FROM body_measurements ORDER BY date").fetchall()
    assert len(rows) == 2
    assert rows[0]['date'] == '2026-06-01'
    assert rows[0]['waist_cm'] == 90.0
    assert rows[0]['hips_cm'] == 100.0
    assert rows[0]['neck_cm'] == 38.0
    
    assert rows[1]['date'] == '2026-06-02'
    assert rows[1]['waist_cm'] == 89.5
    assert rows[1]['hips_cm'] == 99.5
    assert rows[1]['neck_cm'] is None
    
    # Check if measurement_log table exists and is populated
    log_rows = c.execute("SELECT date, type_key, value FROM measurement_log ORDER BY date, type_key").fetchall()
    assert len(log_rows) == 5
    
    conn.close()


def test_measure_commands(temp_db, capsys):
    import argparse
    from scripts.tracker import cmd_measure, cmd_measure_type, cmd_stats_measure
    
    # 1. List default types
    cmd_measure_type(argparse.Namespace(database=str(temp_db), measure_type_command="list"))
    out = capsys.readouterr().out
    assert "waist" in out
    assert "hips" in out
    assert "neck" in out
    
    # 2. Define a custom measurement type
    cmd_measure_type(argparse.Namespace(
        database=str(temp_db), measure_type_command="define", key="chest", name="Chest", unit="in", desc="Chest circumference flexed"
    ))
    out = capsys.readouterr().out
    assert "Measurement type 'chest' defined: Chest (in)" in out
    
    # 3. List types and verify custom type exists
    cmd_measure_type(argparse.Namespace(database=str(temp_db), measure_type_command="list"))
    out = capsys.readouterr().out
    assert "chest" in out
    assert "Chest" in out
    assert "in" in out
    assert "Chest circumference flexed" in out
    
    # 4. Log measurements for the custom type (with optional notes)
    cmd_measure(argparse.Namespace(
        database=str(temp_db), type="chest", value=40.5, date="2026-06-01", today=None, notes="Morning"
    ))
    cmd_measure(argparse.Namespace(
        database=str(temp_db), type="chest", value=41.25, date="2026-06-02", today=None, notes="Evening"
    ))
    out = capsys.readouterr().out
    assert "Chest logged: 40.5 in on 2026-06-01 | notes: Morning" in out
    assert "Chest logged: 41.25 in on 2026-06-02 | notes: Evening" in out
    
    # 5. Get stats for the custom type and check if notes are printed
    cmd_stats_measure(argparse.Namespace(
        database=str(temp_db), type="chest", entries=None, days=None, today="2026-06-02"
    ))
    out = capsys.readouterr().out
    assert "CHEST TRENDS (LAST 5 ENTRIES)" in out
    assert "2026-06-01: 40.5 in | notes: Morning" in out
    assert "2026-06-02: 41.25 in (+0.75 in) | notes: Evening" in out
    assert "Total Change: +0.75 in (from 40.5 to 41.25)" in out
    
    # 6. Delete a measurement type
    cmd_measure_type(argparse.Namespace(
        database=str(temp_db), measure_type_command="delete", key="chest"
    ))
    out = capsys.readouterr().out
    assert "Measurement type 'chest' and all associated log entries deleted." in out



