import sys
sys.path.insert(0, "..")
import pytest
from datetime import date
from database_handler import DatabaseHandler
from data_parser import DataParser
from calculate_stats import StatCalculator

@pytest.fixture
def dietz_scenario_db(tmp_path):
    """
    Creates a database with a specific scenario for testing the Modified Dietz Method:
    Dates are set to the 15th/16th to bypass the allocate_to_month 10th-day cutoff rule.
    - 2017-01-15: Deposit 1000 SEK
    - 2017-01-16: Purchase Asset A for 1000 SEK (locks capital into an asset)
    - 2018-01-15: Sell half (500 SEK) and withdraw 500 SEK on 16th
    - 2019-01-15: Sell remainder (600 SEK - a 100 SEK gain) and withdraw 600 SEK on 16th
    """
    csv_content = """Datum;Konto;Typ av transaktion;Värdepapper/beskrivning;Antal;Kurs;Belopp;Courtage;Valuta;ISIN;Resultat
2017-01-15;1111;Insättning;Deposit;-;-;1000;0;SEK;;-
2017-01-16;1111;Köp;Asset A;100;10;-1000;0;SEK;TESTA;-
2018-01-15;1111;Sälj;Asset A;-50;10;500;0;SEK;TESTA;-
2018-01-16;1111;Uttag;;-;-;-500;0;SEK;;-
2019-01-15;1111;Sälj;Asset A;-50;12;600;0;SEK;TESTA;-
2019-01-16;1111;Uttag;;-;-;-600;0;SEK;;-
"""
    csv_file = tmp_path / "dietz_scenario.csv"
    csv_file.write_text(csv_content, encoding="utf-8")
    
    db_file = tmp_path / "test_modified_dietz.db"
    db = DatabaseHandler(db_file)
    
    parser = DataParser(db)
    parser.add_data(str(csv_file))
    parser.process_transactions()
    
    return db

def test_modified_dietz_weights_and_time_horizon(dietz_scenario_db):
    """
    Tests that the Modified Dietz APY calculation applies multiple weights
    using the aggregated transaction months, and stops the time horizon when the 
    position is fully closed, rather than continuing to the current date.
    """
    stat_calculator = StatCalculator(dietz_scenario_db)
    stat_calculator.calculate_stats()
    
    # Fetch monthly stats including closed positions (deposits="all")
    stats = stat_calculator.get_stats(accounts=["1111"], period="month", deposits="all")
    
    # Look for the cohort originating from Jan 2017
    cohort_2017 = next((s for s in stats if s[0].year == 2017 and s[0].month == 1), None)
    assert cohort_2017 is not None, "2017 cohort should exist"
    
    # Indices based on StatCalculator.get_stats return tuple:
    # 1: deposit, 2: withdrawal, 3: value, 4: total_gainloss, 10: annual_per_yield
    deposit = cohort_2017[1]
    withdrawal = cohort_2017[2]
    value = cohort_2017[3]
    total_gainloss = cohort_2017[4]
    apy = cohort_2017[10]
    
    assert deposit == 1000.0
    assert withdrawal == 1100.0  # 500 + 600
    assert value == 0.0          # Position fully closed
    assert total_gainloss == 100.0
    
    # Mathematical expectation using transaction_month aggregation:
    # Start date: 2017-01-15 (V0 = 1000)
    # End date (fully closed): 2019-01-31 (End of month aggregation, 746 days total)
    #
    # CF1: -500 aggregated to 2018-01-31 (381 days in). Weight = (746 - 381) / 746 = 0.4893
    # CF2: -600 aggregated to 2019-01-31 (746 days in). Weight = (746 - 746) / 746 = 0
    #
    # Sum(W * CF) = 0.4893 * (-500) = -244.65
    # Denominator = V0 + Sum(W * CF) = 1000 - 244.65 = 755.35
    # HPR = Gain / Denominator = 100 / 755.35 ≈ 13.24%
    # Annualized (over 746 days / 365.25 = 2.04 years) = (1 + 0.1324)^(1 / 2.04) - 1 ≈ 6.30%
    
    assert apy is not None, "APY should be calculated for historical positions"
    
    # Asserting approximate APY based on the new monthly-aggregated chronological math
    assert 6.25 <= apy <= 6.35, f"Expected APY around 6.30%, got {apy}%"