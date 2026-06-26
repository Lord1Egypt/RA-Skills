// Test React component with translatable strings

import React from 'react';

function LoginForm() {
  return (
    <div className="login-form">
      <h1>Welcome Back</h1>
      <p>Please sign in to continue</p>
      
      <form>
        <div className="form-group">
          <label>Email Address</label>
          <input 
            type="email" 
            placeholder="Enter your email"
            aria-label="Email input field"
          />
        </div>
        
        <div className="form-group">
          <label>Password</label>
          <input 
            type="password" 
            placeholder="Enter your password"
            aria-label="Password input field"
          />
        </div>
        
        <div className="form-actions">
          <button type="submit">Sign In</button>
          <button type="button">Cancel</button>
        </div>
        
        <p className="forgot-password">
          Forgot your password? <a href="/reset">Reset it here</a>
        </p>
      </form>
      
      <div className="error-message">
        Invalid email or password
      </div>
    </div>
  );
}

export default LoginForm;
