# Script 27: Interview Question Generator

topics = {
    "power": ["Explain load flow", "What is power factor?"],
    "circuit": ["Explain Ohm’s law", "What is Kirchhoff’s law?"]
}

topic = input("Enter topic (power/circuit): ")

for q in topics.get(topic, []):
    print("-", q)
