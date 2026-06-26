import pytest

from datetime import datetime
from data_parser import SpecialCases


# Test that error is raised when the special cases file is missing
def test_parse_special_cases__file_not_found():
    with pytest.raises(FileNotFoundError):
        SpecialCases("non_existing_file.json")

@pytest.fixture(scope='module')
def special_cases():
    return SpecialCases("./test/data/special_cases_test.json")

# Test different conditions for handle_special_cases
def test_handle_special_cases__conditions(special_cases):
    # Test that the function returns changed values when the input matches the special cases
    matching_row = (datetime(2019, 1, 1).date(), 'A', 'B', 'DNB SMB', 'D')
    assert special_cases.handle_special_cases(matching_row) == (datetime(2019, 1, 1).date(), 'A', 'B', 'DNB SMB A', 'D')
    
    # Test that the function returns the same values when the input only matches the first condition
    matching_first_cond = (datetime(2019, 1, 1).date(), 'A', 'B', 'C', 'D')
    assert special_cases.handle_special_cases(matching_first_cond) == matching_first_cond

    # Test that the function returns the same values when the input only matches the second condition
    matching_second_cond = (datetime(2023, 1, 1).date(), 'A', 'B', 'DNB SMB', 'D')
    assert special_cases.handle_special_cases(matching_second_cond) == matching_second_cond 

def test_handle_special_cases__replacements(special_cases):
    # Test that the function replaces one value when matching "One Replacement"
    matching_one_replacement = (datetime(2019, 1, 1).date(),"One Replacement",3,4,5)
    assert special_cases.handle_special_cases(matching_one_replacement) == (datetime(2019, 1, 1).date(),"One Replacement","Replaced",4,5)

    # Test that the function replaces two values when matching "Two Replacements"
    matching_two_replacements = (datetime(2019, 1, 1).date(),"Two Replacements",3,4,5)
    assert special_cases.handle_special_cases(matching_two_replacements) == (datetime(2019, 1, 1).date(),"Two Replacements","Replaced1","Replaced2",5)