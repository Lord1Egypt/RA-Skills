#!/bin/bash
echo "Installing dependencies for BBC Crawler..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies. Please check if Python and pip are installed correctly."
    exit 1
fi
echo "Dependencies installed successfully!"
