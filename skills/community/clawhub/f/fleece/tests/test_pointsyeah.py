from pointsyeah import FlightsQuery, HotelsQuery, build_flights_url, build_hotels_url


def test_flights_url_contains_params():
    url = build_flights_url(FlightsQuery("jfk", "lax", "2026-04-10", adults=2, cabin="business"))
    assert "type=flights" in url
    assert "origin=JFK" in url
    assert "destination=LAX" in url
    assert "date=2026-04-10" in url
    assert "adults=2" in url
    assert "cabin=business" in url


def test_hotels_url_contains_params():
    url = build_hotels_url(HotelsQuery("Jersey City", "2026-04-10", "2026-04-12", guests=2, rooms=1))
    assert "type=hotels" in url
    assert "location=Jersey+City" in url
    assert "checkin=2026-04-10" in url
    assert "checkout=2026-04-12" in url
    assert "guests=2" in url
    assert "rooms=1" in url


def test_flights_return_date():
    url = build_flights_url(FlightsQuery("JFK", "LHR", "2026-06-01", return_date="2026-06-15"))
    assert "return=2026-06-15" in url


def test_flights_no_return_date():
    url = build_flights_url(FlightsQuery("JFK", "LHR", "2026-06-01"))
    assert "return=" in url  # param present but empty
