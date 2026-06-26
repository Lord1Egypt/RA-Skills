import sys

def calculate_position_size(balance, risk_percent, stop_loss_dist):
    """
    Calcule la taille de la position en fonction du risque.
    Formule: (Balance * % Risque) / Distance du Stop Loss
    """
    risk_amount = balance * (risk_percent / 100)
    if stop_loss_dist <= 0:
        return 0
    position_size = risk_amount / stop_loss_dist
    return position_size

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 position_sizing.py <balance> <risk_percent> <stop_loss_dist>")
        sys.exit(1)
    
    try:
        balance = float(sys.argv[1])
        risk_percent = float(sys.argv[2])
        stop_loss_dist = float(sys.argv[3])
        
        size = calculate_position_size(balance, risk_percent, stop_loss_dist)
        print(f"{size:.8f}")
    except ValueError:
        print("Erreur: Les arguments doivent être des nombres.")
        sys.exit(1)
