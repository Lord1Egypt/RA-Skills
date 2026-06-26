# Script 66: Prompt Similarity

def similarity(p1, p2):
    set1 = set(p1.split())
    set2 = set(p2.split())

    return len(set1 & set2) / len(set1 | set2)

p1 = input("Prompt 1: ")
p2 = input("Prompt 2: ")

score = similarity(p1, p2)

print(f"Similarity Score = {score:.2f}")
