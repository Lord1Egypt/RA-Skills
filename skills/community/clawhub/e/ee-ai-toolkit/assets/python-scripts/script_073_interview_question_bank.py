# Script 73: Interview Question Bank

questions = {
    "power": ["What is load flow?", "Explain power factor"],
    "circuit": ["Ohm’s law?", "Kirchhoff laws?"]
}

topic = input("Choose topic (power/circuit): ")

for q in questions.get(topic, []):
    print("-", q)
