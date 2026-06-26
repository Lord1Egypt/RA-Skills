// Flight search functionality for FlightMapify

// Store flight markers and polylines
var flightMarkers = [];
var flightPolylines = [];

// Color palette for different flights
var flightColors = [
    '#6366f1', // Indigo
    '#8b5cf6', // Violet
    '#a855f7', // Purple
    '#d946ef', // Fuchsia
    '#ec4899', // Pink
    '#f43f5e', // Rose
    '#f97316', // Orange
    '#f59e0b', // Amber
    '#eab308', // Yellow
    '#84cc16', // Lime
    '#22c55e', // Green
    '#10b981', // Emerald
    '#14b8a6', // Teal
    '#06b6d4', // Cyan
    '#0ea5e9', // Sky
    '#3b82f6', // Blue
    '#6366f1', // Indigo (repeat)
    '#8b5cf6', // Violet (repeat)
];

// Function to get color for a flight based on index
function getFlightColor(index) {
    return flightColors[index % flightColors.length];
}

// Function to clear existing flight markers and polylines
function clearFlightMarkers() {
    flightMarkers.forEach(function(markerObj) {
        map.remove(markerObj.marker);
    });
    flightMarkers = [];
    
    flightPolylines.forEach(function(polyline) {
        map.remove(polyline);
    });
    flightPolylines = [];
}

// Function to add flight marker and route line
function addFlightMarkerAndRoute(flight, index) {
    // Get unique color for this flight
    var strokeColor = getFlightColor(index);
    
    // Add departure marker
    var depMarker = new AMap.Marker({
        position: [parseFloat(flight.departureLng), parseFloat(flight.departureLat)],
        content: `<div style="width:24px;height:24px;background:${strokeColor};color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;text-shadow:0 1px 1px rgba(0,0,0,0.3);box-shadow:0 2px 6px rgba(0,0,0,0.4);">🛫</div>`,
        offset: new AMap.Pixel(-12, -12),
        zIndex: 85
    });
    
    // Add arrival marker  
    var arrMarker = new AMap.Marker({
        position: [parseFloat(flight.arrivalLng), parseFloat(flight.arrivalLat)],
        content: `<div style="width:24px;height:24px;background:${strokeColor};color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:12px;text-shadow:0 1px 1px rgba(0,0,0,0.3);box-shadow:0 2px 6px rgba(0,0,0,0.4);">🛬</div>`,
        offset: new AMap.Pixel(-12, -12),
        zIndex: 85
    });
    
    // Create flight route polyline - use routePath if available (for connecting flights)
    var routePath = flight.routePath || [
        [parseFloat(flight.departureLng), parseFloat(flight.departureLat)],
        [parseFloat(flight.arrivalLng), parseFloat(flight.arrivalLat)]
    ];
    
    var polyline = new AMap.Polyline({
        path: routePath,
        strokeColor: strokeColor,
        strokeWeight: 3,
        strokeOpacity: 0.8,
        zIndex: 80,
        lineJoin: 'round',
        lineCap: 'round'
    });
    
    // Add transfer markers for connecting flights
    if (flight.routePath && flight.routePath.length > 2) {
        for (var i = 1; i < flight.routePath.length - 1; i++) {
            var transferMarker = new AMap.Marker({
                position: [parseFloat(flight.routePath[i][0]), parseFloat(flight.routePath[i][1])],
                content: `<div style="width:20px;height:20px;background:${strokeColor};color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:10px;text-shadow:0 1px 1px rgba(0,0,0,0.3);box-shadow:0 2px 6px rgba(0,0,0,0.4);">✈️</div>`,
                offset: new AMap.Pixel(-10, -10),
                zIndex: 86
            });
            map.add(transferMarker);
            flightMarkers.push({ marker: transferMarker, type: 'transfer' });
        }
    }
    
    // Create flight info window
    var flightInfo = `<div style="padding:12px; min-width:220px; background:white; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.2);">
        <h4 style="margin:0 0 6px 0; color:${strokeColor}; font-size:14px; font-weight:700;">✈️ ${flight.flightNumber}</h4>
        <p style="margin:0 0 4px 0; font-size:11px; color:#495057;">
            <strong>${flight.origin} → ${flight.destination}</strong>
        </p>
        <p style="margin:0 0 4px 0; font-size:11px; color:#495057;">
            ${flight.departureTime} → ${flight.arrivalTime}
        </p>
        <p style="margin:0 0 4px 0; font-size:12px; color:${strokeColor}; font-weight:600;">${flight.price}</p>
        <p style="margin:0; font-size:10px; color:#6c757d;">航司: ${flight.airline} · ${flight.journeyType || '直达'}</p>
        <div style="margin-top:8px;">
            <a href="${flight.bookingUrl}" target="_blank" style="display:inline-block; padding:6px 12px; background:${strokeColor}; color:white; text-decoration:none; border-radius:4px; font-size:11px; font-weight:600;">预订航班</a>
        </div>
    </div>`;
    
    var infoWindow = new AMap.InfoWindow({
        content: flightInfo,
        autoMove: true,
        offset: new AMap.Pixel(0, -10)
    });
    
    // Click handler for both markers
    function createClickHandler(infoContent) {
        return function() {
            var iw = new AMap.InfoWindow({
                content: infoContent,
                autoMove: true,
                offset: new AMap.Pixel(0, -10)
            });
            iw.open(map, this.getPosition());
        };
    }
    
    depMarker.on('click', createClickHandler(flightInfo));
    arrMarker.on('click', createClickHandler(flightInfo));
    
    // Add to map
    map.add(depMarker);
    map.add(arrMarker);
    map.add(polyline);
    
    flightMarkers.push({ marker: depMarker, type: 'departure' });
    flightMarkers.push({ marker: arrMarker, type: 'arrival' });
    flightPolylines.push(polyline);
}

// Function to display flight in list
function displayFlightInList(flight, index) {
    const flightItem = document.createElement('div');
    flightItem.className = 'flight-item';
    flightItem.style.cursor = 'pointer';
    
    // Get color for this flight
    const strokeColor = getFlightColor(index);
    
    // Build route display with transfer points
    let routeDisplay = '';
    if (flight.routeCities && flight.routeCities.length > 2) {
        // Connecting flight - show A->B->C format
        const routeStr = flight.routeCities.join(' → ');
        routeDisplay = `<span style="font-size:9px; color:#64748b;">${routeStr}</span>`;
    } else {
        routeDisplay = `<span style="font-size:10px; color:#64748b;">${flight.origin} → ${flight.destination}</span>`;
    }
    
    flightItem.innerHTML = `
        <div class="flight-icon" style="background:${strokeColor};">✈️</div>
        <div class="flight-info">
            <strong style="color:${strokeColor};">${flight.flightNumber}</strong><br>
            ${routeDisplay}<br>
            <span style="font-size:10px; color:#64748b;">${flight.departureTime} → ${flight.arrivalTime} · ${flight.price}</span>
            <span class="flight-type" style="color:${strokeColor};">${flight.journeyType || '直达'}</span>
        </div>
    `;
    
    // Add click event to center map on departure airport
    flightItem.onclick = function() {
        const flightPosition = [parseFloat(flight.departureLng), parseFloat(flight.departureLat)];
        map.setCenter(flightPosition);
        map.setZoom(6);
        
        // Find and open the corresponding marker's info window
        const flightMarker = flightMarkers.find(m => 
            Math.abs(m.marker.getPosition().getLng() - parseFloat(flight.departureLng)) < 0.0001 &&
            Math.abs(m.marker.getPosition().getLat() - parseFloat(flight.departureLat)) < 0.0001
        );
        
        if (flightMarker) {
            const infoWindow = new AMap.InfoWindow({
                content: `<div style="padding:12px; min-width:220px; background:white; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.2);">
                    <h4 style="margin:0 0 6px 0; color:#6366f1; font-size:14px; font-weight:700;">✈️ ${flight.flightNumber}</h4>
                    <p style="margin:0 0 4px 0; font-size:11px; color:#495057;">
                        <strong>${flight.origin} → ${flight.destination}</strong>
                    </p>
                    <p style="margin:0 0 4px 0; font-size:11px; color:#495057;">
                        ${flight.departureTime} → ${flight.arrivalTime}
                    </p>
                    <p style="margin:0 0 4px 0; font-size:12px; color:#6366f1; font-weight:600;">${flight.price}</p>
                    <p style="margin:0; font-size:10px; color:#6c757d;">航司: ${flight.airline} · ${flight.journeyType || '直达'}</p>
                    <div style="margin-top:8px;">
                        <a href="${flight.bookingUrl}" target="_blank" style="display:inline-block; padding:6px 12px; background:#6366f1; color:white; text-decoration:none; border-radius:4px; font-size:11px; font-weight:600;">预订航班</a>
                    </div>
                </div>`,
                autoMove: true,
                offset: new AMap.Pixel(0, -10)
            });
            
            infoWindow.open(map, flightMarker.marker.getPosition());
        }
    };
    
    return flightItem;
}

// Function to display flights on map AND in list
function displayFlightsOnMapAndList(flights) {
    // Clear existing flight markers and routes
    clearFlightMarkers();
    
    const flightResultsSection = document.getElementById('flightResultsSection');
    const flightResultsList = document.getElementById('flightResultsList');
    
    if (!flights || flights.length === 0) {
        flightResultsSection.style.display = 'none';
        showNotification('未找到相关航班');
        return;
    }
    
    // Clear flight list
    flightResultsList.innerHTML = '';
    
    // Add flight markers to map and items to list (show top 10)
    const displayFlights = flights.slice(0, 10);
    displayFlights.forEach(function(flight, index) {
        // Add to map
        addFlightMarkerAndRoute(flight, index + 1);
        
        // Add to list
        const flightItem = displayFlightInList(flight, index + 1);
        flightResultsList.appendChild(flightItem);
    });
    
    // Show flight results section
    flightResultsSection.style.display = 'block';
    
    // Zoom to show both origin and destination
    if (flights.length > 0) {
        const firstFlight = flights[0];
        const bounds = new AMap.Bounds(
            [parseFloat(firstFlight.departureLng), parseFloat(firstFlight.departureLat)],
            [parseFloat(firstFlight.arrivalLng), parseFloat(firstFlight.arrivalLat)]
        );
        map.setBounds(bounds, {padding: [50, 50, 50, 50]});
    }
    
    // Show success message
    showNotification(`已找到 ${flights.length} 个航班！地图和列表中显示了前10个航班。`, false);
}

// Function to validate flight search inputs
function validateFlightInputs(origin, destination, departureDate) {
    if (!origin || !destination) {
        return '请输入出发地和目的地';
    }
    
    if (!departureDate) {
        return '请选择旅行日期';
    }
    
    // Validate date format
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(departureDate)) {
        return '日期格式无效，请使用 YYYY-MM-DD 格式';
    }
    
    // Check if departure date is in the past
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const departure = new Date(departureDate);
    if (departure < today) {
        return '旅行日期不能是过去日期';
    }
    
    return null;
}

// Function to show notification
function showNotification(message, isError = true) {
    const notificationArea = document.getElementById('notificationArea');
    notificationArea.textContent = message;
    notificationArea.style.color = isError ? '#e74c3c' : '#27ae60';
    notificationArea.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        notificationArea.style.display = 'none';
    }, 3000);
}

// Main flight search function
function searchFlights() {
    const flightSearchBtn = document.getElementById('flightSearchBtn');
    
    // Check if button is already disabled (search in progress)
    if (flightSearchBtn.disabled) {
        return;
    }
    
    const origin = document.getElementById('flightOrigin').value.trim();
    const destination = document.getElementById('flightDestination').value.trim();
    const departureDate = document.getElementById('flightDepartureDate').value;
    
    // Validate inputs
    const validationError = validateFlightInputs(origin, destination, departureDate);
    if (validationError) {
        console.log('Flight search validation error:', validationError);
        showNotification(validationError);
        return;
    }
    
    // Update button state
    flightSearchBtn.textContent = '搜索中...';
    flightSearchBtn.disabled = true;
    flightSearchBtn.style.opacity = '0.6';
    flightSearchBtn.style.cursor = 'not-allowed';
    
    // Build URL with parameters
    let url = `http://localhost:8791/api/flight-search?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}&departure-date=${departureDate}`;
    
    // Set up timeout to re-enable button after 10 seconds
    const timeoutId = setTimeout(() => {
        flightSearchBtn.textContent = '搜航班';
        flightSearchBtn.disabled = false;
        flightSearchBtn.style.opacity = '1';
        flightSearchBtn.style.cursor = 'pointer';
    }, 10000);
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Clear timeout since we got a response
            clearTimeout(timeoutId);
            
            // Restore button state
            flightSearchBtn.textContent = '搜航班';
            flightSearchBtn.disabled = false;
            flightSearchBtn.style.opacity = '1';
            flightSearchBtn.style.cursor = 'pointer';
            
            if (data.error) {
                console.log('Flight search error:', data.error);
                showNotification(`航班查询失败: ${data.error}`);
            } else if (data.flights && Array.isArray(data.flights)) {
                // Display flights directly on the map
                displayFlightsOnMapAndList(data.flights);
            } else {
                console.log('Unexpected flight data:', data);
                showNotification('未找到相关航班数据');
            }
        })
        .catch(error => {
            // Clear timeout since we got an error
            clearTimeout(timeoutId);
            
            // Restore button state
            flightSearchBtn.textContent = '搜航班';
            flightSearchBtn.disabled = false;
            flightSearchBtn.style.opacity = '1';
            flightSearchBtn.style.cursor = 'pointer';
            
            console.error('Flight search error:', error);
            showNotification('航班查询失败，请检查网络连接');
        });
}

// Allow Enter key to trigger flight search in origin field
document.getElementById('flightOrigin').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchFlights();
    }
});

// Allow Enter key to trigger flight search in destination field
document.getElementById('flightDestination').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchFlights();
    }
});