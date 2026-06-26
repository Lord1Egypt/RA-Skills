"""
My Credit Cards Page for Fleece Application

This module implements the personal credit card management page of the Fleece application.
It allows users to track, add, edit, and analyze their existing credit cards portfolio.

Features:
- View all current credit cards with detailed information
- Add new cards using templates or custom information
- Edit existing card details
- Remove cards no longer in use
- Sort cards by name, annual fee, credit limit, or date added
- View portfolio insights with visualizations
- Performance optimizations including:
  - Cached data loading
  - Pagination for improved performance
  - Parallel image loading
  - Lazy loading with collapsed expanders

Author: @chenyuan99
Date: May 2025
"""
import datetime
import os
import sys

import pandas as pd
import streamlit as st

# Ensure project root is on sys.path so db.py is importable from the pages/ dir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import db
from image_service import display_card_image
# Set page configuration
st.set_page_config(page_title="My Credit Cards | Fleece", layout="wide")

# Load custom CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Try with relative path from pages directory
        try:
            with open(os.path.join(os.path.dirname(__file__), "..", "style.css")) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load custom styling: {e}")

try:
    load_css()
except Exception as e:
    st.warning(f"Could not load custom styling: {e}")

# Page header
st.title("My Credit Cards")
st.subheader("Manage your current credit card portfolio")

@st.cache_data(ttl=300)
def load_user_cards():
    """Load cards from SQLite with a 5-minute cache."""
    try:
        return db.get_cards()
    except Exception as e:
        st.error(f"Error loading your cards: {e}")
        return []

# Load user's credit cards
user_cards = load_user_cards()

# Two tabs: View Cards and Add New Card
tab1, tab2 = st.tabs(["My Cards", "Add New Card"])

# Tab 1: View Cards
with tab1:
    if not user_cards:
        st.info("You haven't added any credit cards yet. Use the 'Add New Card' tab to add your first card.")
    else:
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Cards", len(user_cards))
        with col2:
            total_credit_limit = sum(card.get('credit_limit', 0) for card in user_cards)
            st.metric("Total Credit Limit", f"${total_credit_limit:,}")
        with col3:
            annual_fees = sum(int(card.get('annual_fee', '0').replace('$', '').replace(',', '')) for card in user_cards)
            st.metric("Annual Fees", f"${annual_fees}")
        
        # Sort options
        sort_by = st.selectbox(
            "Sort by",
            options=["Card Name", "Annual Fee", "Credit Limit", "Date Added"],
            index=0
        )
        
        # Sort the cards based on selection
        if sort_by == "Card Name":
            sorted_cards = sorted(user_cards, key=lambda x: x.get('name', ''))
        elif sort_by == "Annual Fee":
            sorted_cards = sorted(user_cards, key=lambda x: int(x.get('annual_fee', '$0').replace('$', '').replace(',', '')))
        elif sort_by == "Credit Limit":
            sorted_cards = sorted(user_cards, key=lambda x: x.get('credit_limit', 0), reverse=True)
        else:  # Date Added
            sorted_cards = sorted(user_cards, key=lambda x: x.get('date_added', ''), reverse=True)
        
        # Preload card images in parallel for better performance
        @st.cache_data(ttl=3600)
        def preload_my_card_images(cards, max_cards=5):
            """
            Preload user's credit card images in parallel for improved performance.
            
            This function uses Python's concurrent.futures module to fetch multiple card images
            simultaneously, which significantly improves loading performance compared to
            sequential loading. It only preloads a limited number of images (default: 5) to
            balance initial load time with memory usage.
            
            Args:
                cards (list): List of user's card dictionaries containing image_url keys
                max_cards (int, optional): Maximum number of cards to preload. Defaults to 5.
                    Increasing this value will preload more images initially but may slow down
                    the initial page load.
            
            Returns:
                dict: A dictionary mapping image URLs to their corresponding PIL Image objects
            
            Performance Notes:
                - Uses ThreadPoolExecutor for parallel fetching
                - Limited to 5 concurrent workers to avoid overwhelming the network
                - Results are cached for 1 hour using Streamlit's caching
                - Only preloads the first few cards for optimal initial page load time
                - Silently handles errors to avoid disrupting the UI
            """
            import concurrent.futures
            
            # Only preload the first few cards for initial performance
            urls = [card.get('image_url', '') for card in cards[:max_cards] if card.get('image_url')]
            
            results = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {executor.submit(display_card_image, url): url for url in urls}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        results[url] = future.result()
                    except Exception as e:
                        pass  # Silently handle errors
            
            return results
        
        # Preload images for better performance
        preloaded_images = preload_my_card_images(sorted_cards)
        
        # Show initial number of cards with pagination
        if 'cards_page' not in st.session_state:
            st.session_state.cards_page = 0
        
        cards_per_page = 3
        start_idx = st.session_state.cards_page * cards_per_page
        end_idx = min(start_idx + cards_per_page, len(sorted_cards))
        
        # Display pagination controls
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.session_state.cards_page > 0:
                if st.button("← Previous"):
                    st.session_state.cards_page -= 1
                    st.rerun()
        
        with col2:
            st.write(f"Showing cards {start_idx + 1}-{end_idx} of {len(sorted_cards)}")
        
        with col3:
            if end_idx < len(sorted_cards):
                if st.button("Next →"):
                    st.session_state.cards_page += 1
                    st.rerun()
        
        # Display cards for current page
        for i, card in enumerate(sorted_cards[start_idx:end_idx], start_idx):
            with st.expander(f"**{card['name']}**", expanded=False):  # Use collapsed by default for better performance
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Use preloaded image if available, otherwise fetch on demand
                    if card.get('image_url') in preloaded_images:
                        img = preloaded_images[card.get('image_url')]
                    else:
                        img = display_card_image(card.get('image_url', ''))
                        
                    if img:
                        st.image(img, width=250)
                
                with col2:
                    # Card details
                    st.markdown(f"### {card['name']}")
                    st.markdown(f"**Card Number:** •••• •••• •••• {card.get('last_four', '****')}")
                    st.markdown(f"**Annual Fee:** {card.get('annual_fee', 'N/A')}")
                    st.markdown(f"**Credit Limit:** ${card.get('credit_limit', 'N/A'):,}")
                    st.markdown(f"**Rewards:** {card.get('rewards', 'N/A')}")
                    st.markdown(f"**Expiration:** {card.get('expiration', 'N/A')}")
                    st.markdown(f"**Date Added:** {card.get('date_added', 'N/A')}")
                    
                    # Action buttons in a form to reduce rerendering
                    with st.container():
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Remove Card", key=f"remove_{i}"):
                                db.remove_card(card['name'])
                                st.success(f"Removed {card['name']} from your cards!")
                                load_user_cards.clear()
                                st.rerun()
                        
                        with col2:
                            if st.button(f"Edit Details", key=f"edit_{i}"):
                                st.session_state['edit_card'] = card
                                st.session_state['edit_index'] = i
                                st.rerun()
        
        # Edit card form (appears when Edit Details is clicked)
        if 'edit_card' in st.session_state and 'edit_index' in st.session_state:
            with st.form("edit_card_form"):
                st.subheader(f"Edit {st.session_state['edit_card']['name']}")
                
                name = st.text_input("Card Name", value=st.session_state['edit_card']['name'])
                last_four = st.text_input("Last Four Digits", value=st.session_state['edit_card'].get('last_four', ''))
                annual_fee = st.text_input("Annual Fee (e.g. $95)", value=st.session_state['edit_card'].get('annual_fee', '$0'))
                credit_limit = st.number_input("Credit Limit ($)", value=int(st.session_state['edit_card'].get('credit_limit', 0)))
                rewards = st.text_area("Rewards", value=st.session_state['edit_card'].get('rewards', ''))
                expiration = st.text_input("Expiration (MM/YY)", value=st.session_state['edit_card'].get('expiration', ''))
                
                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    db.update_card(st.session_state['edit_card']['name'], {
                        "last_four":    last_four,
                        "annual_fee":   annual_fee,
                        "credit_limit": credit_limit,
                        "rewards":      rewards,
                        "expiration":   expiration,
                    })
                    st.success("Card details updated successfully!")
                    load_user_cards.clear()
                    del st.session_state['edit_card']
                    del st.session_state['edit_index']
                    st.rerun()

# Tab 2: Add New Card
with tab2:
    st.subheader("Add a New Credit Card")
    
    # Sample card templates to choose from
    card_templates = [
        {"name": "Chase Sapphire Preferred", "annual_fee": "$95", "rewards": "5x on travel purchased through Chase, 3x on dining, 2x on other travel", "image_url": "https://creditcards.chase.com/K-Marketplace/images/cardart/sapphire_preferred_card.png"},
        {"name": "American Express Gold", "annual_fee": "$250", "rewards": "4x at restaurants, 4x at U.S. supermarkets (up to $25,000/year), 3x on flights", "image_url": "https://icm.aexp-static.com/Internet/Acquisition/US_en/AppContent/OneSite/category/cardarts/gold-card.png"},
        {"name": "Citi Double Cash", "annual_fee": "$0", "rewards": "2% on all purchases (1% when you buy, 1% when you pay)", "image_url": "https://www.citi.com/CRD/images/citi-double-cash/card_2.png"},
        {"name": "Capital One Venture", "annual_fee": "$95", "rewards": "2x miles on all purchases", "image_url": "https://ecm.capitalone.com/WCM/card/products/venture-card-art/tablet.png"},
        {"name": "Custom Card", "annual_fee": "$0", "rewards": "Enter your own rewards", "image_url": ""}
    ]
    
    # Let user select from templates or custom
    template_names = [card["name"] for card in card_templates]
    selected_template = st.selectbox("Select a card template or create custom", template_names)
    
    # Get the selected template
    template = next((card for card in card_templates if card["name"] == selected_template), None)
    
    # Create a form for adding a new card
    with st.form("add_card_form"):
        name = st.text_input("Card Name", value=template["name"])
        last_four = st.text_input("Last Four Digits", max_chars=4, help="Last 4 digits of your card number")
        annual_fee = st.text_input("Annual Fee", value=template["annual_fee"])
        credit_limit = st.number_input("Credit Limit ($)", min_value=0, value=10000, step=1000)
        rewards = st.text_area("Rewards", value=template["rewards"])
        expiration = st.text_input("Expiration Date (MM/YY)", placeholder="05/28")
        
        # Only show image URL field for custom card
        image_url = template["image_url"]
        if selected_template == "Custom Card":
            image_url = st.text_input("Card Image URL (optional)")
        
        submitted = st.form_submit_button("Add Card")
        if submitted:
            new_card = {
                "name":         name,
                "last_four":    last_four,
                "annual_fee":   annual_fee,
                "credit_limit": credit_limit,
                "rewards":      rewards,
                "expiration":   expiration,
                "image_url":    image_url,
                "date_added":   datetime.datetime.now().strftime("%Y-%m-%d"),
            }
            try:
                db.add_card(new_card)
                load_user_cards.clear()
                st.success(f"Added {name} to your cards!")
                st.rerun()
            except ValueError:
                st.error(f'"{name}" is already in your cards.')

# Add a section for card statistics and insights
if user_cards:
    st.markdown("---")
    st.header("Card Portfolio Insights")
    
    # Create dataframe for analysis
    card_data = []
    for card in user_cards:
        annual_fee_value = int(card.get('annual_fee', '$0').replace('$', '').replace(',', ''))
        card_data.append({
            'name': card.get('name', 'Unknown'),
            'annual_fee': annual_fee_value,
            'credit_limit': card.get('credit_limit', 0)
        })
    
    df = pd.DataFrame(card_data)
    
    # Display charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Credit Limit Distribution")
        st.bar_chart(df.set_index('name')['credit_limit'])
    
    with col2:
        st.subheader("Annual Fee Comparison")
        st.bar_chart(df.set_index('name')['annual_fee'])
    
    # Calculate utilization if we had that data
    st.info("💡 Pro tip: A good credit utilization ratio is under 30% of your total available credit.")

# Footer
st.markdown("---")
st.markdown("© 2025 Fleece | Manage your credit cards wisely.")
