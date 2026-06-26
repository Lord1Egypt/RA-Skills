# Script 76: Certification Tracker

certs = []

while True:
    c = input("Enter certification (or 'exit'): ")

    if c == "exit":
        break

    certs.append(c)

print("\nCertifications:")
for c in certs:
    print("-", c)
