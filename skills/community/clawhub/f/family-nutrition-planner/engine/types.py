"""
Type definitions for Family Nutrition Planner
"""

from typing import Literal, Optional
from typing_extensions import TypedDict


class GenderType(TypedDict):
    gender: Literal["male", "female", "other"]


class ActivityLevelType(TypedDict):
    activityLevel: Literal["sedentary", "lightly-active", "moderately-active", "very-active", "extra-active"]


class GoalType(TypedDict):
    type: Literal["balance", "low-carb", "high-protein", "weight-loss", "muscle-gain"]


class FamilyMember(TypedDict):
    name: str
    age: int
    gender: GenderType
    weight: float  # kg
    height: float  # cm
    activityLevel: ActivityLevelType
    goals: Optional[list[str]]
    allergies: Optional[list[str]]


class Preferences(TypedDict, total=False):
    cuisine: list[str]
    cookingStyle: list[str]
    avoid: list[str]


class Constraints(TypedDict, total=False):
    weeklyBudget: float
    maxPrepTime: int
    servingSize: int


class NutritionPlanRequest(TypedDict):
    familyName: Optional[str]
    members: list[FamilyMember]
    preferences: Optional[Preferences]
    constraints: Optional[Constraints]
    goals: Optional[GoalType]


class MacronutrientBalance(TypedDict):
    protein: str
    carbohydrates: str
    fat: str


class NutritionSummary(TypedDict):
    averageDailyCalories: float
    macronutrientBalance: MacronutrientBalance
    foodVariety: int


class MealInfo(TypedDict):
    name: str
    calories: int
    prepTime: str
    ingredients: list[str]


class Meals(TypedDict):
    breakfast: MealInfo
    lunch: MealInfo
    dinner: MealInfo
    snacks: Optional[list[MealInfo]]


class DailyMacros(TypedDict):
    calories: int
    protein: str
    carbohydrates: str
    fat: str


class DailyPlan(TypedDict):
    day: str
    meals: Meals
    dailyNutrition: DailyMacros


class CategoryItem(TypedDict):
    category: str
    items: list[dict]  # Simplified


class ShoppingList(TypedDict):
    categories: list[CategoryItem]
    estimatedCost: int
    savingsTips: list[str]


class NutritionAnalysis(TypedDict):
    strengths: list[str]
    concerns: list[str]
    suggestions: list[str]


class NutritionPlanReport(TypedDict):
    success: bool
    nutritionSummary: NutritionSummary
    dailyPlans: list[DailyPlan]
    shoppingList: ShoppingList
    nutritionAnalysis: NutritionAnalysis
    weeklyNutritionTrend: str
