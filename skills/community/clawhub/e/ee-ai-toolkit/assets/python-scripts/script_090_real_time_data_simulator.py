# Script 90: Real-Time Data Simulation

import time
import random

for i in range(10):
    value = random.uniform(200, 240)
    print(f"Voltage Reading: {value:.2f} V")
    time.sleep(1)
