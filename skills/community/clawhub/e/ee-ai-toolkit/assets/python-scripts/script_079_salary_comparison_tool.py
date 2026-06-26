# Script 79: Salary Comparison

salaries = list(map(float, input("Enter salaries: ").split()))

print("Max Salary:", max(salaries))
print("Min Salary:", min(salaries))
print("Average Salary:", sum(salaries)/len(salaries))
