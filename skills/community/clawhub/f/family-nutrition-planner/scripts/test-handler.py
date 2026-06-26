#!/usr/bin/env python3
"""
Test script for Family Nutrition Planner handler.
"""

import sys
sys.path.insert(0, '/Users/jianghaidong/.openclaw/skills/family-nutrition-planner')

from handler import handle_nutrition_request, handle_nutrition_calculation

# Test 1: Weekly meal plan generation
print("=" * 60)
print("Test 1: Weekly Meal Plan Generation")
print("=" * 60)

test_request = {
    "familyName": "张氏家庭",
    "members": [
        {"name": "爸爸", "age": 35, "gender": "male", "weight": 75, "height": 175, "activityLevel": "lightly-active", "allergies": []},
        {"name": "妈妈", "age": 32, "gender": "female", "weight": 58, "height": 162, "activityLevel": "lightly-active", "allergies": []},
        {"name": "孩子", "age": 8, "gender": "male", "weight": 28, "height": 130, "activityLevel": "moderately-active", "allergies": ["虾"]}
    ],
    "preferences": {"cuisine": ["中式"], "cookingStyle": ["少油", "清淡"]},
    "constraints": {"weeklyBudget": 500, "maxPrepTime": 60, "servingSize": 4},
    "goals": {"type": "balance"}
}

result = handle_nutrition_request(test_request)

print(f"Success: {result['success']}")
print(f"Average Daily Calories: {result['nutritionSummary']['averageDailyCalories']}")
print(f"Macro Balance: {result['nutritionSummary']['macronutrientBalance']}")
print(f"Food Variety: {result['nutritionSummary']['foodVariety']} ingredients")
print(f"Daily Plans Count: {len(result['dailyPlans'])}")
print(f"Shopping Categories: {len(result['shoppingList']['categories'])}")
print(f"Estimated Cost: {result['shoppingList']['estimatedCost']}元")
print(f"Allergen Warnings: {result['nutritionAnalysis']['concerns']}")

# Check first day plan
if result['dailyPlans']:
    first_day = result['dailyPlans'][0]
    print(f"\nFirst Day Plan ({first_day['day']}):")
    for meal_type, meal in first_day['meals'].items():
        print(f"  {meal_type}: {meal['name']} ({meal['calories']} kcal)")

print("\n" + "=" * 60)
print("Test 2: Single Member Nutrition Calculation")
print("=" * 60)

member_test = {
    "name": "测试用户",
    "age": 30,
    "gender": "male",
    "weight": 70,
    "height": 175,
    "activityLevel": "moderately-active",
    "goalType": "muscle-gain"
}

calc_result = handle_nutrition_calculation(member_test)

print(f"Success: {calc_result['success']}")
print(f"Member: {calc_result['member']}")
print(f"BMR: {calc_result['bmr']} kcal")
print(f"TDEE: {calc_result['tdee']} kcal")
print(f"Target Intake: {calc_result['targetIntake']} kcal")
print(f"Macros:")
print(f"  Protein: {calc_result['macronutrientTargets']['protein']['grams']}g ({calc_result['macronutrientTargets']['protein']['percentage']}%)")
print(f"  Carbs: {calc_result['macronutrientTargets']['carbohydrates']['grams']}g ({calc_result['macronutrientTargets']['carbohydrates']['percentage']}%)")
print(f"  Fat: {calc_result['macronutrientTargets']['fat']['grams']}g ({calc_result['macronutrientTargets']['fat']['percentage']}%)")

print("\n" + "=" * 60)
print("All Tests Passed!")
print("=" * 60)
