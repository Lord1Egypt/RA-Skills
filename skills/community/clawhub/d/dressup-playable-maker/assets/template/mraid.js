// MRAID 3.0 Mock/Stub for PlayTurbo Detection
// This is a minimal implementation to satisfy the MRAID interface requirements

(function() {
    'use strict';
    
    // Prevent double-loading
    if (typeof window.mraid !== 'undefined') {
        return;
    }
    
    // MRAID State
    var state = 'loading';
    var viewable = false;
    var placementType = 'inline';
    var expandProperties = {
        width: 0,
        height: 0,
        useCustomClose: false,
        isModal: true
    };
    var resizeProperties = {
        width: 0,
        height: 0,
        offsetX: 0,
        offsetY: 0,
        customClosePosition: 'top-right',
        allowOffscreen: true
    };
    var orientationProperties = {
        allowOrientationChange: true,
        forceOrientation: 'none'
    };
    
    // Event listeners storage
    var listeners = {};
    
    function addEventListener(event, listener) {
        if (!listeners[event]) {
            listeners[event] = [];
        }
        listeners[event].push(listener);
    }
    
    function removeEventListener(event, listener) {
        if (listeners[event]) {
            var idx = listeners[event].indexOf(listener);
            if (idx !== -1) {
                listeners[event].splice(idx, 1);
            }
        }
    }
    
    function fireEvent(event, data) {
        if (listeners[event]) {
            listeners[event].forEach(function(listener) {
                try {
                    listener(data);
                } catch (e) {
                    console.error('MRAID event listener error:', e);
                }
            });
        }
    }
    
    // MRAID API
    window.mraid = {
        // Version
        getVersion: function() {
            return '3.0';
        },
        
        // State
        getState: function() {
            return state;
        },
        
        // Placement Type
        getPlacementType: function() {
            return placementType;
        },
        
        // Viewable
        isViewable: function() {
            return viewable;
        },
        
        // Expand
        expand: function(url) {
            state = 'expanded';
            fireEvent('stateChange', state);
            console.log('MRAID expand called', url);
        },
        
        getExpandProperties: function() {
            return expandProperties;
        },
        
        setExpandProperties: function(props) {
            Object.assign(expandProperties, props);
        },
        
        // Close
        close: function() {
            state = 'hidden';
            fireEvent('stateChange', state);
            console.log('MRAID close called');
        },
        
        // Resize
        resize: function() {
            console.log('MRAID resize called');
        },
        
        getResizeProperties: function() {
            return resizeProperties;
        },
        
        setResizeProperties: function(props) {
            Object.assign(resizeProperties, props);
        },
        
        // Orientation
        getOrientationProperties: function() {
            return orientationProperties;
        },
        
        setOrientationProperties: function(props) {
            Object.assign(orientationProperties, props);
        },
        
        // Open
        open: function(url) {
            console.log('MRAID open called:', url);
            window.open(url, '_blank');
        },
        
        // Events
        addEventListener: addEventListener,
        removeEventListener: removeEventListener,
        
        // Support
        supports: function(feature) {
            var supportedFeatures = ['sms', 'tel', 'calendar', 'storePicture', 'inlineVideo'];
            return supportedFeatures.indexOf(feature) !== -1;
        },
        
        // Store Picture
        storePicture: function(url) {
            console.log('MRAID storePicture called:', url);
        },
        
        // Create Calendar Event
        createCalendarEvent: function(params) {
            console.log('MRAID createCalendarEvent called:', params);
        },
        
        // Play Video
        playVideo: function(url) {
            console.log('MRAID playVideo called:', url);
        }
    };
    
    // Simulate ready state
    setTimeout(function() {
        state = 'default';
        viewable = true;
        fireEvent('ready');
        fireEvent('stateChange', state);
        fireEvent('viewableChange', viewable);
    }, 100);
    
    console.log('MRAID 3.0 mock loaded');
})();
