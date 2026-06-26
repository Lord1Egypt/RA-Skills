# Script 42: Peak Load Detector

loads = list(map(float, input("Enter load values: ").split()))

peak = max(loads)
index = loads.index(peak)

print(f"Peak Load = {peak} MW at position {index}")
