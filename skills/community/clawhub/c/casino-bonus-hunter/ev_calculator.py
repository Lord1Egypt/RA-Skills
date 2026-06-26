"""
EV Calculator pour les bonus casino
EV = Bonus - (Wagering x House Edge)
"""

# House edge par jeu (avec strategie optimale)
HOUSE_EDGE = {
    "blackjack": 0.003,        # 0.3% - basic strategy
    "blackjack_h17": 0.005,    # 0.5% - dealer hits soft 17
    "video_poker_job": 0.0046, # 0.46% - JoB 9/6
    "video_poker_dw": -0.0076, # -0.76% - Deuces Wild full pay (joueur gagne)
    "baccarat_banker": 0.0106, # 1.06%
    "baccarat_player": 0.0124, # 1.24%
    "roulette_eu": 0.027,      # 2.7% - europeenne
    "roulette_us": 0.0526,     # 5.26% - americaine
    "craps_passline": 0.0141,  # 1.41%
    "slots": 0.04,             # 4% - moyenne
}

def calculate_ev(
    bonus_amount: float,
    wagering_multiplier: float,
    game: str = "blackjack",
    game_contribution: float = 1.0,
    max_win: float = None,
    deposit_required: float = 0
) -> dict:
    """
    Calcule l'Expected Value d'un bonus casino.

    bonus_amount: montant du bonus en $
    wagering_multiplier: x fois le bonus a jouer (ex: 30 = x30)
    game: jeu utilise pour le wagering
    game_contribution: % de contribution au wagering (1.0 = 100%, 0.1 = 10%)
    max_win: plafond de gain maximum (None si pas de limite)
    deposit_required: depot minimum requis

    Returns: dict avec EV, rating, details
    """
    edge = HOUSE_EDGE.get(game, 0.04)

    # Wagering reel apres contribution
    real_wagering = (bonus_amount * wagering_multiplier) / game_contribution

    # Perte attendue sur le wagering
    expected_loss = real_wagering * edge

    # EV brut
    ev_gross = bonus_amount - expected_loss

    # Ajuster si max_win
    if max_win is not None:
        ev_gross = min(ev_gross, max_win)

    # EV net (deduire depot si requis)
    ev_net = ev_gross

    # Rating
    if ev_net > 80:
        rating = "EXCELLENT"
        stars = 5
    elif ev_net > 50:
        rating = "BON"
        stars = 4
    elif ev_net > 20:
        rating = "MOYEN"
        stars = 3
    elif ev_net > 0:
        rating = "FAIBLE"
        stars = 2
    else:
        rating = "NEGATIF - SKIP"
        stars = 0

    return {
        "bonus": bonus_amount,
        "wagering_x": wagering_multiplier,
        "real_wagering": round(real_wagering, 2),
        "game": game,
        "game_contribution_pct": int(game_contribution * 100),
        "house_edge_pct": round(edge * 100, 2),
        "expected_loss": round(expected_loss, 2),
        "ev_gross": round(ev_gross, 2),
        "ev_net": round(ev_net, 2),
        "max_win": max_win,
        "rating": rating,
        "stars": stars,
    }

def score_bonus(bonus: dict) -> float:
    """Score un bonus pour le ranking. Plus le score est haut, meilleur le bonus."""
    ev = bonus.get("ev_net", 0)
    if ev <= 0:
        return -9999
    # Bonus: penaliser les wagering trop eleves (risque variance)
    wager_penalty = max(0, (bonus.get("wagering_x", 30) - 30) * 0.5)
    return ev - wager_penalty


# Tests
if __name__ == "__main__":
    examples = [
        {"name": "BitStarz Welcome", "bonus": 100, "wager": 30, "game": "blackjack", "contrib": 1.0, "max_win": None},
        {"name": "PlayAmo 50% Reload", "bonus": 50, "wager": 40, "game": "blackjack", "contrib": 0.1, "max_win": 200},
        {"name": "Casino X 200% Slots", "bonus": 100, "wager": 35, "game": "slots", "contrib": 1.0, "max_win": 500},
        {"name": "Casumo Cashback 10%", "bonus": 50, "wager": 5, "game": "blackjack", "contrib": 1.0, "max_win": None},
        {"name": "BOE Casino Scam", "bonus": 100, "wager": 60, "game": "slots", "contrib": 1.0, "max_win": 100},
    ]
    
    print(f"{'Casino':<25} {'Bonus':>6} {'Wager':>6} {'EV Net':>8} {'Rating':<15} Stars")
    print("-" * 75)
    for ex in examples:
        r = calculate_ev(ex["bonus"], ex["wager"], ex["game"], ex["contrib"], ex["max_win"])
        print(f"{ex['name']:<25} ${r['bonus']:>5} {r['wagering_x']:>5}x {r['ev_net']:>+7.2f}$ {r['rating']:<15} {'*' * r['stars']}")
