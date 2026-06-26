from setuptools import setup
import py2app

setup(
    app=["desktop-app.py"],
    name="FitDietKernel",
    version="1.0.0",
    description="健身饮食桌面应用",
    app_category="public.app-category.healthcare-fitness",
)
