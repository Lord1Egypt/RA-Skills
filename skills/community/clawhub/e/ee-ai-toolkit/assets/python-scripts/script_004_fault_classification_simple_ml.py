# Script 4: Fault Classification

from sklearn.tree import DecisionTreeClassifier

# Sample data: [current, voltage]
X = [[10, 220], [50, 200], [80, 180]]
y = ["Normal", "Line Fault", "Short Circuit"]

model = DecisionTreeClassifier()
model.fit(X, y)

test = [[60, 190]]
prediction = model.predict(test)

print(f"Predicted Fault Type: {prediction[0]}")
